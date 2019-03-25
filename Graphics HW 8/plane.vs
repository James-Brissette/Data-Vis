#version 330 core

layout(location = 0) in vec3 pos;
layout(location = 1) in vec2 aTexCoord;

uniform mat4 trans;
uniform mat4 depthTrans;

out vec3 fragPosition;
out vec4 depthPosition;
out vec3 normals;
out vec2 texCoord;


void main()
{
	gl_Position = trans * vec4(pos, 1);
	fragPosition = pos;
	texCoord = aTexCoord;

	mat4 dTrans = mat4(0.5, 0, 0, 0,
		0, 0.5, 0, 0,
		0, 0, 0.5, 0,
		0.25, 0.25, 0.5, 1) * depthTrans; 
	depthPosition = dTrans * vec4(pos,1);
}