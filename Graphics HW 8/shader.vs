#version 330 core

layout(location = 0) in vec3 pos;
layout(location = 1) in vec2 aTexCoord;
layout(location = 2) in vec3 vertexNormals;
layout(location = 3) in vec3 surfaceNormals;

uniform mat4 trans;
uniform mat4 depthTrans;

out vec3 fragPosition;
out vec3 normals;
out vec2 texCoord;
out vec4 depthPosition;

void main()
{
	gl_Position = trans * vec4(pos, 1);
	fragPosition = pos;
	
	normals = vertexNormals;

	mat4 dTrans = mat4(0.5, 0, 0, 0,
		0, 0.5, 0, 0,
		0, 0, 0.5, 0,
		0.5, 0.5, 0.49999, 1) * depthTrans; 
	depthPosition = dTrans * vec4(pos,1);
	texCoord = aTexCoord;
}