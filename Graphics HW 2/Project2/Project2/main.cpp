#include <GL/glew.h>
#include <GL/freeglut.h>
#include <iostream>
#include <cyCore.h>
#include <cyPoint.h>
#include <cyMatrix.h>
#include <cyTriMesh.h>
#include <cyGL.h>
#include <glm/glm.hpp>
#include <glm/ext.hpp>

using namespace std;

cy::TriMesh teapot;
cy::GLSLProgram ShaderProgram;
cy::GLSLShader vertexShaderObj;
cy::GLSLShader fragmentShaderObj;
cy::Matrix4f model;
cy::Matrix4f view;
cy::Matrix4f projection;
cy::Point3f target;
int r = 0;
int g = 0;
int b = 0;
int shaderVersion = 1;
float transValues;
float rotationOrigin = -1;
float zoomOrigin = -1;
float xdelta = 0;
float ydelta = 0;
float rx = 0;
float zz = 0;
float rz = 0;
float xangle = 0;
float xzoom = 0;
GLuint transID;

void Idle()
{
	glClearColor(r,g,b, 1.0f);
	glutPostRedisplay();
}

void recompileShaders() {
	cout << "Brace yourselves..\n";
	bool success;
	if (shaderVersion == 1) {
		cout << "Loading Vertex Shader B... ";
		success = vertexShaderObj.CompileFile("shader_b.vs", GL_VERTEX_SHADER);
		if (!success) {
			cout << " Load Failed :( Exiting...\n";
			exit(0);
		}
		else
		{
			cout << "success!\n";
		}

		cout << "Loading Fragment Shader B... ";
		success = fragmentShaderObj.CompileFile("shader_b.fs", GL_FRAGMENT_SHADER);
		if (!success) {
			cout << " Load Failed :( Exiting...\n";
			exit(0);
		}
		else
		{
			cout << "success!\n";
		}
		shaderVersion = 2;
		r = 1;
		g = 1;
		b = 1;
	}
	else
	{
		cout << "Loading Vertex Shader A... ";
		success = vertexShaderObj.CompileFile("shader.vs", GL_VERTEX_SHADER);
		if (!success) {
			cout << " Load Failed :( Exiting...\n";
			exit(0);
		}
		else
		{
			cout << "success!\n";
		}

		cout << "Loading Fragment Shader A... ";
		success = fragmentShaderObj.CompileFile("shader.fs", GL_FRAGMENT_SHADER);
		if (!success) {
			cout << " Load Failed :( Exiting...\n";
			exit(0);
		}
		else
		{
			cout << "success!\n";
		}
		shaderVersion = 1;
		r = 0;
		g = 0;
		b = 0;
	}
	ShaderProgram.CreateProgram();
	ShaderProgram.AttachShader(vertexShaderObj);
	ShaderProgram.AttachShader(fragmentShaderObj);

	GLuint progID = ShaderProgram.GetID();
	transID = glGetUniformLocation(progID, "trans");

	ShaderProgram.Link();
	ShaderProgram.Bind();


	glutPostRedisplay();
}

void Display()
{
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

	projection.SetPerspective(45, 1, 0, .1);
	cy::Matrix4f t;
	t.SetIdentity();

	t = projection * view * model * t;
	t.Get(&transValues);
	glUniformMatrix4fv(transID, 1, GL_FALSE, &transValues);

	glDrawArrays(GL_POINTS, 0, teapot.NV());

	glutSwapBuffers();
}

void Keyboard(unsigned char key, int x, int y)
{
	switch (key)
	{
	case(27):
		glutLeaveMainLoop();
		break;
	case(GLUT_KEY_F6):
	case(-97):
	case(117):
		cout << "hit!\n";
		
		break;
	default:
		break;
	}
}

void SpecialKeys(int key, int x, int y)
{
	switch (key)
	{
	case GLUT_KEY_F6:
		recompileShaders();
		break;
	default:
		break;
	}
}

//Derived the basic structure of these functions from an article on http://www.lighthouse3d.com
//I'm new to C++ so I don't claim to have thought up the following two functions on my own.
void MousePress(int side, int direction, int x, int y)
{
	if (side == GLUT_LEFT_BUTTON)
	{
		if (direction == GLUT_DOWN)
		{
			rotationOrigin = x;
		}
		else
		{
			rotationOrigin = -1;
			xangle += xdelta;
		}
	}

	if (side == GLUT_RIGHT_BUTTON)
	{
		if (direction == GLUT_DOWN)
		{
			zoomOrigin = x;
		}
		else
		{
			zoomOrigin = -1;
			xzoom += xdelta;
		}
	}
}

void MouseDrag(int x, int y)
{
	if (rotationOrigin >= 0) 
	{
		xdelta = (x - rotationOrigin) / GLUT_SCREEN_WIDTH;
		cout << "xdelta: " << xdelta;
		rz = xangle + xdelta;

		model.SetRotationZYX(0.0f, 0.0f, rz);

		glutPostRedisplay();
	}
	else if (zoomOrigin >= 0) 
	{
		xdelta = (x - rotationOrigin) / GLUT_SCREEN_WIDTH * 5;
		cout << "xdelta: " << xdelta;
		zz = xangle + xdelta;

		view.SetView(cyPoint3f(20+zz, 20+zz, 20+zz), target, cyPoint3f(0,0,1));
		glutPostRedisplay();
	}
}

int main(int argc, char* argv[]) {

	char const* const input = argv[1];

	// Initialize GLUT
	glutInit(&argc, argv);
	// Create Window
	glutInitDisplayMode(GL_RGB | GL_DOUBLE);
	glutInitWindowSize(1000, 1000);
	glEnable(GL_DEPTH_TEST);
	glutCreateWindow("Transformations");

	bool test = teapot.LoadFromFileObj(input);
	
	GLenum res = glewInit();
	if (res != GLEW_OK)
	{
		fprintf(stderr, "Error: '%s'\n", glewGetErrorString(res));
		return 1;
	}

	GLuint VAO;
	glGenVertexArrays(1, &VAO);
	glBindVertexArray(VAO);
	// Generate 1 buffer using the address of the Global GLuint Object
	GLuint VBO;
	glGenBuffers(1, &VBO);
	
	// Bind all subsequent commands to our new buffer
	glBindBuffer(GL_ARRAY_BUFFER, VBO);

	//Fill it with data
	glBufferData(GL_ARRAY_BUFFER, teapot.NV()*sizeof(cy::Point3f), &teapot.V(0), GL_STATIC_DRAW);

	//Enable Attrib
	glEnableVertexAttribArray(0);

	//Before Drawing, bind again (good practice)
	glBindBuffer(GL_ARRAY_BUFFER, VBO);
	glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, 0);
	//trans

	ShaderProgram.CreateProgram();
	vertexShaderObj.CompileFile("shader.vs", GL_VERTEX_SHADER);
	fragmentShaderObj.CompileFile("shader.fs", GL_FRAGMENT_SHADER);

	ShaderProgram.AttachShader(vertexShaderObj);
	ShaderProgram.AttachShader(fragmentShaderObj);
	GLuint progID = ShaderProgram.GetID();
	transID = glGetUniformLocation(progID, "trans");

	ShaderProgram.Link();
	ShaderProgram.Bind();


	teapot.ComputeBoundingBox();
	cy::Point3f max = teapot.GetBoundMax();
	cy::Point3f min = teapot.GetBoundMin();
	target = (max + min) / 2;
	cy::Point3f up = cy::Point3f(0, 0, 1);

	cout << "BB Max: " << max.x << "," << max.y << "," << max.z << " and Min: " << min.x << "," << min.y << "," << min.z;
	cout << "\nAverage: " << target.x << "," << target.y << "," << target.z;

	cy::Matrix4f t;
	t.SetIdentity();
	model.SetRotationZYX(0, 0, 3.14);

	cout << "\nData: ";
	for (int i = 0; i < 16; i++) {
		cout << model.data[i] << ",";
	}
	
	
	view.SetView(cy::Point3f(20,20,20), target, up);
	projection.SetPerspective(1.57, 1, 0.1, 50);
	t = projection * view * model * t;

	t.Get(&transValues);
	glUniformMatrix4fv(transID, 1, GL_FALSE, &transValues);

	glutDisplayFunc(Display);
	glutIdleFunc(Idle);
	glutKeyboardFunc(Keyboard);
	glutSpecialFunc(SpecialKeys);
	glutMouseFunc(MousePress);
	glutMotionFunc(MouseDrag);

	
	glutPostRedisplay();
	glutMainLoop();
	return 0;
}