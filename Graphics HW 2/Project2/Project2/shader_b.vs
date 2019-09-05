#version 330 core
layout(location = 0) in vec3 pos;

uniform mat4 trans;
out vec4 vcolor;

void main()
{
	gl_Position = trans * vec4(pos, 1);
	vcolor = vec4(0, 0, 0, 1.0f);
}