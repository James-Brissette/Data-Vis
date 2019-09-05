#version 330 core

layout(location = 0) in vec3 pos;

out vec4 fragPosition;
uniform mat4 trans;

void main()
{
	gl_Position = trans * vec4(pos, 1);
}