#include <GL/glew.h>
#include <GL/freeglut.h>
#include <iostream>
#include <cyCore.h>
#include <cyPoint.h>
#include <cyMatrix.h>
#include <cyTriMesh.h>
#include <cyGL.h>
#include <lodepng.h>

using namespace std;

cy::TriMesh teapot, cube, sphere;
cy::TriMesh::Mtl m;
cy::GLSLProgram ShaderProgram;
cy::GLSLShader vertexShaderObj, fragmentShaderObj;
cy::GLSLProgram planeProgram;
cy::GLSLShader planeVS, planeFS;
cy::GLSLProgram cubeProgram;
cy::GLSLShader cubeVS, cubeFS;
cy::GLSLProgram meshProgram;
cy::GLSLShader meshVS, meshFS, meshGS, meshTCS, meshTES;
cy::GLSLProgram depthProgram;
cy::GLSLShader depthVS, depthFS;
cy::Matrix4f model, planeModel;
cy::Matrix4f view, planeView;
cy::Matrix4f projection, depthProjection;
cy::Point3f pos, planePos;
cy::Point3f lightPos, planeLightPos;
cy::Point3f target, planeTarget;
cy::Point3f up;
cy::GLRenderTexture<GL_TEXTURE_2D> renderTex;
cy::GLRenderDepth<GL_TEXTURE_2D> renderDepth;

//Texture Variables
std::vector<unsigned char> image0;
unsigned tex0Width, tex0Height;
unsigned int texture0;


int shaderVersion = 1;
int displayMesh = 1;
float r = 0;
float g = 0;
float b = 0;
float pi;
float transValues[16], depthValues[16];
float viewValues[16];
float rotationOrigin = -1;
float zoomOrigin = -1;
float xdelta = 0, planeXDelta = 0;
float lightDelta = 0, planeLightDelta = 0;
float rx = 0;
float ry = 0;
float lightRy = 0, planeLightRy = 0;
float rz = 0;
float zz = 0;
float translationZ = 0;
float xangle = 0, planeXAngle = 0;
float lightAngle = 0, planeLightAngle = 0;
float xzoom = 0, planeXZoom = 0;

GLuint VAO[4]; //teapot, plane, cube, sphere
GLuint VBO[4];
GLuint bufferID;

const unsigned int SHADOW_WIDTH = 4000, SHADOW_HEIGHT = 4000;
const unsigned int SCREEN_WIDTH = 800, SCREEN_HEIGHT = 800;


void updateTex();
void Idle()
{
	glClearColor(r, g, b, 1.0f);
	glClearDepth(1.0f);
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

	glutPostRedisplay();
}

void Display()
{
	//projection.SetPerspective(45, 1, 0.1, 10.0);
	//projection.SetIdentity();

	cy::Matrix4f t;
	t.SetIdentity();


	//PLANE
	/*glBindVertexArray(VAO[1]);
	planeProgram.Bind();
	model.SetIdentity();
	t = projection * view * model * t;
	t.Get(transValues);

	planeProgram.SetUniformMatrix4(0, transValues);
	planeProgram.SetUniform(1, pos);
	planeProgram.SetUniform(2, 1);
	planeProgram.SetUniform(3, lightPos);
	planeProgram.SetUniformMatrix4(4, depthValues);

	glDrawArrays(GL_TRIANGLES, 0, 6);*/

	//MESH
	if (displayMesh) {
		glBindVertexArray(VAO[3]);
		meshProgram.Bind();
		model.SetIdentity();
		t.SetIdentity();
		t = projection * view * model * t;
		t.Get(transValues);

		meshProgram.SetUniformMatrix4(0, transValues);
		meshProgram.SetUniform(1, pos);
		meshProgram.SetUniform(2, 1);
		meshProgram.SetUniform(3, lightPos);
		meshProgram.SetUniformMatrix4(4, depthValues);

		glPatchParameteri(GL_PATCH_VERTICES, 3);
		glPatchParameteri(GL_PATCH_DEFAULT_OUTER_LEVEL, 2);
		glPatchParameteri(GL_PATCH_DEFAULT_INNER_LEVEL, 2);
		glDrawArrays(GL_TRIANGLES, 0, 6);
	}

	//TEAPOT
	/*glBindVertexArray(VAO[0]);
	ShaderProgram.Bind();
	model.SetIdentity();
	t.SetScale(cyPoint3f(.5, .5, .5));
	t = projection * view * model * t;
	t.Get(transValues);

	ShaderProgram.SetUniformMatrix4(0, transValues);
	ShaderProgram.SetUniformMatrix4(1, depthValues);
	ShaderProgram.SetUniform(5, pos);
	ShaderProgram.SetUniform(12, 1);

	glDrawArrays(GL_TRIANGLES, 0, 3 * teapot.NF());*/


	//LIGHT
	glDepthMask(GL_FALSE);
	glBindVertexArray(VAO[2]);
	cubeProgram.Bind();
	model.SetTrans(lightPos);
	t.SetScale(cyPoint3f(.1, .1, .1));
	t = projection * view * model * t;
	t.Get(transValues);

	cubeProgram.SetUniformMatrix4(0, transValues);

	glDrawArrays(GL_TRIANGLES, 0, 36);
	glDepthMask(GL_TRUE);

	glBindVertexArray(0);

	glutSwapBuffers();
}

void Keyboard(unsigned char key, int x, int y)
{
	switch (key)
	{
	case(27):
		glutLeaveMainLoop();
		break;
	case(32):
		if (displayMesh) { displayMesh = 0; }
		else { displayMesh = 1; }
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
		printf("Recompile Shaders Disabled\n");
		//recompileShaders();
		break;
	default:
		break;
	}
}

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
			planeXAngle += planeXDelta;

			lightAngle += lightDelta;
			planeLightAngle += planeLightDelta;
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
			planeXZoom += planeXDelta;
		}
	}
}

void MouseDrag(int x, int y)
{
	if (glutGetModifiers() == 2) //CTRL KEY PRESSED DURING DRAG
	{
		lightDelta = (x - rotationOrigin) / GLUT_SCREEN_WIDTH;
		xdelta = 0;
		lightRy = lightAngle + lightDelta;

		lightPos = cyPoint3f(10 * cos(lightRy), 15.0f,	10 * sin(lightRy));

		ShaderProgram.Bind();
		ShaderProgram.SetUniform(2, lightPos);
		
	}
	/*else if (glutGetModifiers() == 4) //ALT KEY PRESSED DURING DRAG
	{
		if (rotationOrigin >= 0) //Control Rotation on left click
		{
			planeXDelta = (x - rotationOrigin) / GLUT_SCREEN_WIDTH;
			planeLightDelta = 0;
			ry = planeXAngle + planeXDelta;

			planePos = cyPoint3f(15 * cos(ry), 10.0f, 15 * sin(ry));
			planeView.SetView(planePos, planeTarget, up);
			//model.SetRotationZYX(rx, ry, 0.0f);
			//model.SetTransComponent(cyPoint3f(0, 0, -10));

			glutPostRedisplay();
		}
		else if (zoomOrigin >= 0) //Control Zoom on right click
		{
			planeXDelta = (x - rotationOrigin) / GLUT_SCREEN_WIDTH * 5;
			zz = planeXAngle + planeXDelta;

			planePos = cyPoint3f(15 * cos(ry), 10.0f, 15 * sin(ry) + 10 * zz);
			planeView.SetView(planePos, planeTarget, up);
			glutPostRedisplay();
		}	
		
	}*/
	else if (rotationOrigin >= 0)
	{
		xdelta = (x - rotationOrigin) / GLUT_SCREEN_WIDTH;
		lightDelta = 0;
		ry = xangle + xdelta;

		pos = cyPoint3f(30 * cos(ry), 10.0f, 30 * sin(ry));
		view.SetView(pos, target, up);

	}
	else if (zoomOrigin >= 0)
	{
		xdelta = (x - rotationOrigin) / GLUT_SCREEN_WIDTH * 5;
		//cout << "xdelta: " << xdelta;
		zz = xangle + xdelta;

		pos = cyPoint3f(30 * cos(ry), 10.0f, 30 * sin(ry) + 10 * zz);
		view.SetView(pos, target, up);

	}

	updateTex();
	glutPostRedisplay();
}

void updateBgColor(float rd, float gn, float bl) {
	r = rd;
	g = gn;
	b = bl;
}

void updateTex() {
	
	glViewport(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);
	renderDepth.Bind(); 

	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
	renderDepth.BindTexture(1);
	//depthProgram.Bind();
	
	glClearDepth(1.0f);
	glClear(GL_DEPTH_BUFFER_BIT);

	//:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::;
	cy::Matrix4f t;
	t.SetIdentity();

	view.SetView(lightPos * 2, target, up);

	//TEAPOT
	glBindVertexArray(VAO[0]);
	ShaderProgram.Bind();
	model.SetIdentity();
	t.SetScale(.5);
	t = projection * view * model * t;
	t.Get(transValues);

	cyMatrix4f bias = cyMatrix4f(0.5, 0, 0, 0.25,
		0, 0.5, 0, 0.25,
		0, 0, 0.5, 0.4999,
		0, 0, 0, 1);


	bias = bias * t;
	t.Get(depthValues);

	cy::Matrix4f v;
	v.SetIdentity();
	v.Get(viewValues);

	ShaderProgram.SetUniformMatrix4(0, transValues);
	ShaderProgram.SetUniformMatrix4(1, viewValues);
	ShaderProgram.SetUniform(2, lightPos);
	ShaderProgram.SetUniform(5, pos);

	glDrawArrays(GL_TRIANGLES, 0, 3 * teapot.NF());

	//:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::;

	bufferID = renderTex.GetID();
	
	renderDepth.Unbind();
	view.SetView(pos, target, up);
	glViewport(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);



	//glutPostRedisplay();
}

struct VData {
	cyPoint3f position;
	cyPoint3f vertexNormal;
	cyPoint3f surfaceNormal;
	cyPoint3f texCoord;
};

struct Plane {
	cyPoint3f position;
	cyPoint3f texCoord;
};

struct Cube {
	cyPoint3f position;
};

struct Sphere {
	cyPoint3f position;
	cyPoint3f vertexNormal;
};

int main(int argc, char* argv[]) {

	char const* const input = argv[1];

	// Initialize GLUT
	glutInit(&argc, argv);
	// Create Window
	glutInitDisplayMode(GLUT_RGBA | GLUT_ALPHA | GLUT_DOUBLE | GLUT_DEPTH);
	glutInitWindowSize(SCREEN_WIDTH, SCREEN_HEIGHT);
	glutInitContextVersion(4, 2);
	glutInitContextProfile(GLUT_CORE_PROFILE);

	//glDisable(GL_CULL_FACE);
	//glCullFace(GL_FALSE);

	glDepthFunc(GL_LEQUAL);

	glutCreateWindow("Shadow Mapping");
	GLenum res = glewInit();
	if (res != GLEW_OK)
	{
		fprintf(stderr, "Error: '%s'\n", glewGetErrorString(res));
		return 1;
	}

		
	char const* const cubeFilePath = "cube.obj";
	teapot.LoadFromFileObj(input);
	cube.LoadFromFileObj(cubeFilePath);


	/*Rotations, Translations, Perspectives*/
	rx = 0;
	translationZ = -10;
	pi = 3.141592653589793238462643383279502884197169;

	teapot.ComputeBoundingBox();
	cy::Point3f max = teapot.GetBoundMax();
	cy::Point3f min = teapot.GetBoundMin();
	cyPoint3f center = (max + min) / 2;

	pos = cy::Point3f(0, 10, 30);
	target = center*.5;// cyPoint3f(0, 5, 0);
	up = cy::Point3f(0, 1, 0);


	cy::Matrix4f t;
	cy::Matrix4f v;

	t.SetIdentity();
	t.SetScale(cyPoint3f(.5, .5, .5));
	v.SetIdentity();


	model.SetRotationZYX(0, 0, 0);
	view.SetView(pos, target, up);
	projection.SetPerspective(pi / 2, 1.0f, 0.1f, 55.0f);
	

	t = projection * view * model * t;
	v = view * model;

	t.Get(transValues);
	v.Get(viewValues);

	v.Invert();
	v.Transpose();
	vector<VData> theGoods(3 * teapot.NF());
	cyPoint3f bc;
	cyTriMesh::TriFace f;
	cyTriMesh::TriFace fn;
	cyTriMesh::TriFace ft;
	cyPoint3f U;
	cyPoint3f V;
	cyPoint3f N;

	// TEAPOT
	for (int i = 0; i < teapot.NF(); i++) {
		f = teapot.F(i);
		fn = teapot.FN(i);
		ft = teapot.FT(i);

		for (int j = 0; j < 3; j++) {
			theGoods[3 * i + j].position = teapot.V(f.v[j]);
			theGoods[3 * i + j].vertexNormal = v.VectorTransform(teapot.VN(fn.v[j])).GetNormalized();
			theGoods[3 * i + j].texCoord = teapot.VT(ft.v[j]);
		}

		U = theGoods[3 * i + 1].position - theGoods[3 * i].position;
		V = theGoods[3 * i + 2].position - theGoods[3 * i].position;
		N = cyPoint3f(U.y*V.z - U.z*V.y, U.z*V.x - U.x*V.z, U.x*V.y - U.y*V.x);
		v.VectorTransform(N);

		theGoods[3 * i].surfaceNormal = N.GetNormalized();
		theGoods[3 * i + 1].surfaceNormal = N.GetNormalized();
		theGoods[3 * i + 2].surfaceNormal = N.GetNormalized();
	}

	//CUBE
	vector<Cube> cubeData(3 * cube.NF());
	for (int i = 0; i < cube.NF(); i++) {
		f = cube.F(i);
		fn = teapot.FN(i);
		for (int j = 0; j < 3; j++) {
			cubeData[3 * i + j].position = cube.V(f.v[j]);
			v.VectorTransform(teapot.VN(fn.v[j])).GetNormalized();
		}
	}


	//PLANE
	vector<Plane> plane(6);
	plane[0].position = cyPoint3f(-10, 10, 0);
	plane[0].texCoord = cyPoint3f(0, 0, 0);
	plane[1].position = cyPoint3f(10, 10, 0);
	plane[1].texCoord = cyPoint3f(1, 0, 0);
	plane[2].position = cyPoint3f(10, -10, 0);
	plane[2].texCoord = cyPoint3f(1, 1, 0);
	plane[3].position = cyPoint3f(10, -10, 00);
	plane[3].texCoord = cyPoint3f(1, 1, 0);
	plane[4].position = cyPoint3f(-10, -10, 0);
	plane[4].texCoord = cyPoint3f(0, 1, 0);
	plane[5].position = cyPoint3f(-10, 10, 0);
	plane[5].texCoord = cyPoint3f(0, 0, 0);

	vector<cyPoint3f> textureVertices;

	
	/*:::::::::::::::::::::::::::::    VERTEX ARRAYS    ::::::::::::::::::::::::::::::*/
	glGenVertexArrays(4, VAO);
	glGenBuffers(4, VBO);

	//TEAPOT
	glBindVertexArray(VAO[0]); 
	glBindBuffer(GL_ARRAY_BUFFER, VBO[0]);
	glBufferData(GL_ARRAY_BUFFER, theGoods.size() * sizeof(VData), theGoods.data(), GL_STATIC_DRAW);
	glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, sizeof(VData), 0);
	glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, sizeof(VData), (GLvoid*)offsetof(VData, texCoord)); 
	glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, sizeof(VData), (GLvoid*)offsetof(VData, vertexNormal));
	glVertexAttribPointer(3, 3, GL_FLOAT, GL_FALSE, sizeof(VData), (GLvoid*)offsetof(VData, surfaceNormal));
	
	glEnableVertexAttribArray(0);
	glEnableVertexAttribArray(1);
	glEnableVertexAttribArray(2);
	glEnableVertexAttribArray(3);

	//PLANE
	glBindVertexArray(VAO[1]);
	glBindBuffer(GL_ARRAY_BUFFER, VBO[1]);
	glBufferData(GL_ARRAY_BUFFER, plane.size() * sizeof(Plane), plane.data(), GL_STATIC_DRAW);
	glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, sizeof(Plane), 0);
	glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, sizeof(Plane), (GLvoid*)offsetof(Plane, texCoord));
	
	glEnableVertexAttribArray(0);
	glEnableVertexAttribArray(1);

	//CUBE
	glBindVertexArray(VAO[2]);
	glBindBuffer(GL_ARRAY_BUFFER, VBO[2]);
	glBufferData(GL_ARRAY_BUFFER, cubeData.size() * sizeof(Cube), cubeData.data(), GL_STATIC_DRAW);
	glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, sizeof(Cube), 0);

	glEnableVertexAttribArray(0);

	//MESH
	glBindVertexArray(VAO[3]);
	glBindBuffer(GL_ARRAY_BUFFER, VBO[3]);
	glBufferData(GL_ARRAY_BUFFER, plane.size() * sizeof(Plane), plane.data(), GL_STATIC_DRAW);
	glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, sizeof(Plane), 0);
	glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, sizeof(Plane), (GLvoid*)offsetof(Plane, texCoord));

	glEnableVertexAttribArray(0);
	glEnableVertexAttribArray(1);
		
	glBindVertexArray(VAO[0]);
	glEnable(GL_DEPTH_TEST);
	/*::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::*/

	planeProgram.CreateProgram();
	planeVS.CompileFile("plane.vs", GL_VERTEX_SHADER);
	planeFS.CompileFile("plane.fs", GL_FRAGMENT_SHADER);
	planeProgram.AttachShader(planeVS);
	planeProgram.AttachShader(planeFS);
	planeProgram.Link();
	planeProgram.Bind();
	planeProgram.RegisterUniforms("trans cameraPos shadowMap lightPos depthTrans");

	depthProgram.CreateProgram();
	depthVS.CompileFile("depth.vs", GL_VERTEX_SHADER);
	depthFS.CompileFile("depth.fs", GL_FRAGMENT_SHADER);
	depthProgram.AttachShader(depthVS);
	depthProgram.AttachShader(depthFS);
	depthProgram.Link();
	depthProgram.Bind();
	depthProgram.RegisterUniforms("trans");

	cubeProgram.CreateProgram();
	cubeVS.CompileFile("light.vs", GL_VERTEX_SHADER);
	cubeFS.CompileFile("light.fs", GL_FRAGMENT_SHADER);
	cubeProgram.AttachShader(cubeVS);
	cubeProgram.AttachShader(cubeFS);
	cubeProgram.Link();
	cubeProgram.Bind();
	cubeProgram.RegisterUniforms("trans");

	meshProgram.CreateProgram();
	meshVS.CompileFile("plane.vs", GL_VERTEX_SHADER);
	meshFS.CompileFile("mesh.fs", GL_FRAGMENT_SHADER);
	meshGS.CompileFile("mesh.gs", GL_GEOMETRY_SHADER);
	meshTCS.CompileFile("mesh.tcs", GL_TESS_CONTROL_SHADER);
	meshTES.CompileFile("mesh.tes", GL_TESS_EVALUATION_SHADER);
	meshProgram.AttachShader(meshVS);
	meshProgram.AttachShader(meshFS);
	meshProgram.AttachShader(meshGS);
	//meshProgram.AttachShader(meshTCS);
	//meshProgram.AttachShader(meshTES);
	meshProgram.Link();
	meshProgram.Bind();
	meshProgram.RegisterUniforms("trans cameraPos shadowMap lightPos depthTrans");
	

	ShaderProgram.CreateProgram();
	vertexShaderObj.CompileFile("shader.vs", GL_VERTEX_SHADER);
	fragmentShaderObj.CompileFile("shader.fs", GL_FRAGMENT_SHADER);
	ShaderProgram.AttachShader(vertexShaderObj);
	ShaderProgram.AttachShader(fragmentShaderObj);
	GLuint progID = ShaderProgram.GetID();
	ShaderProgram.Link();
	ShaderProgram.Bind();
	ShaderProgram.RegisterUniforms("trans depthTrans lightPos lightColor objColor viewPos texture0 texture1 texture2 Ka Kd Ks shadowMap");

	ShaderProgram.SetUniformMatrix4(0, transValues);
	ShaderProgram.SetUniformMatrix4(1, viewValues);

	lightPos = cyPoint3f(10.0, 15.0, 0);
	ShaderProgram.SetUniform(2, lightPos);
	ShaderProgram.SetUniform(3, 1.0f, 1.0f, 1.0f);

	cyPoint3f objColor = cyPoint3f(0.8f, 0, 0);
	ShaderProgram.SetUniform(4, objColor.x, objColor.y, objColor.z);
	ShaderProgram.SetUniform(5, pos);



	/*:::::::::::::::::::::::::::: Textures ::::::::::::::::::::::::::::*/
	
	unsigned error = lodepng::decode(image0, tex0Width, tex0Height, "teapot_normal.png");
	if (error) std::cout << "decoder error " << error << ": " << lodepng_error_text(error) << std::endl;

	/*error = lodepng::decode(image1, tex1Width, tex1Height, "brick-specular.png");
	if (error) std::cout << "decoder error " << error << ": " << lodepng_error_text(error) << std::endl;
	*/
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);

	glGenTextures(1, &texture0);
	glActiveTexture(GL_TEXTURE0);
	glBindTexture(GL_TEXTURE_2D, texture0);
	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, tex0Width, tex0Height, 0, GL_RGBA, GL_UNSIGNED_BYTE, &image0[0]);
	glGenerateMipmap(GL_TEXTURE_2D);

	//glGenTextures(1, &texture1);
	//resetTextures();

	/*:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::*/
	
	m = teapot.M(0);

	ShaderProgram.SetUniform(6, 0);
	ShaderProgram.SetUniform(7, 1);
	ShaderProgram.SetUniform(8, 2);

	ShaderProgram.SetUniform(9, (cyPoint3f)m.Ka);
	ShaderProgram.SetUniform(10, (cyPoint3f)m.Kd);
	ShaderProgram.SetUniform(11, (cyPoint3f)m.Ks);
	ShaderProgram.SetUniform(12, 2);


	cout << "Ka: (" << m.Ka[0] << "," << m.Ka[1] << "," << m.Ka[2] << ")" << endl;
	cout << "Kd: (" << m.Kd[0] << "," << m.Kd[1] << "," << m.Kd[2] << ")" << endl;
	cout << "Ks: (" << m.Ks[0] << "," << m.Ks[1] << "," << m.Ks[2] << ")" << endl;

	/*::::::::::::::::::::::::::: Cube Map :::::::::::::::::::::::::::::*/

	//ShaderProgram.SetUniform(12, 3); //Bind cubemap texture to uniform

	//renderEnvironment();
	
	/*::::::::::::::::::::::::::: RenderTexture ::::::::::::::::::::::::*/

	//glActiveTexture(GL_TEXTURE2);
	//res = renderDepth.Initialize(true, SHADOW_WIDTH, SHADOW_HEIGHT);
	
	//if (!res) {
	//	cout << "RenderBuffer failed to Initialize\n " << endl;
	//}
	//updateTex();

	/*::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::*/

	glPatchParameteri(GL_PATCH_VERTICES, 3);


	//Good Practice
	glBindVertexArray(VAO[0]);

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