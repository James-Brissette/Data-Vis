#version 330 core

in vec3 fragPosition;
in vec2 texCoord;
in vec4 depthPosition;
//in vec2 pTexCoord;
in vec3 normals;


out vec4 fcolor;
uniform vec3 lightPos;
uniform vec3 lightColor;
uniform vec3 objColor;
uniform vec3 viewPos;
uniform vec3 Ka;
uniform vec3 Kd;
uniform vec3 Ks;
uniform sampler2D texture0;
uniform sampler2D texture1;
uniform sampler2D texture2;

uniform sampler2DShadow shadowMap;

const int lightIntensity = 10;

void main()
{
	float f = textureProj(shadowMap, depthPosition);
	float ratio = 1.00 / 1.52;
	vec3 I = normalize(fragPosition - viewPos);
	vec3 R = reflect(I, normals);
	//vec3 R = refract(I, normals, ratio);

	//Ambient Lighting
	//vec3 ambient = Ka * 0.2;
	vec3 ambient = vec3(1,.1,.1) * 0.3;
	//refract// vec3 ambient = texture(skyBox, R).rgb;

	//Diffuse Lighting
	vec3 lightDir = normalize(lightPos - fragPosition);
	float d = max(dot(normals, lightDir), 0.0);
	//vec3 diffuse = d * Kd;
	vec3 diffuse = d * vec3(1,0,0);// 0.2 is too low, 1 is too high

	//Specular Lighting
	vec3 viewDir = normalize(viewPos - fragPosition);
	vec3 halfDir = normalize(lightDir + viewDir);
	int exp = 32;
	
	//float amp = lightIntensity / length(lightDir);

	float specAngle = max(dot(halfDir, normals), 0.0);
	float specular = pow(specAngle, exp);

	vec3 result = (ambient + diffuse * f) + (specular * vec3(1, 1, 1))*0.5; 
	//refract//vec3 result = (ambient + diffuse) + (specular * vec3(1, 1, 1))*0.5; 

	//fcolor = vcolor;
	fcolor = vec4(result, 1);
	//fcolor = vec4(vec3(gl_FragCoord.z),1);
	//vec3 dir = vec3(.5425, 3.9375,.00154) - fragPosition;
	//fcolor = vec4(texture(skyBox, R).rgb, 1.0);
}



