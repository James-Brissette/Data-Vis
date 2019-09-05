#version 330 core
in vec3 fragPosition;
in vec2 texCoord;
in vec4 gl_FragCoord;
in vec4 depthPosition;
out vec4 fcolor;

uniform vec3 cameraPos;
uniform vec3 lightPos;
uniform sampler2D normalMap;

void main()
{

	//float f = texture(shadowMap,texCoord).r;
	//float f = textureProj(shadowMap,depthPosition * vec4(2,2,1,1));
	//if (f > 1) f=0;
	
	float f = 1.0;
	vec3 N = texture(normalMap,texCoord).rgb;
	vec3 normals = normalize(N * 2 - 1);
	vec4 ambient = vec4(1.0, 1.0, 1.0, 1.0) * 0;

	vec3 lightDir = normalize(lightPos - fragPosition);
	float d = max(dot(normals, lightDir), 0.0);
	vec3 diffuse = d * vec3(1,1,1)*0.5;// 0.2 is too low, 1 is too high

	//Specular Lighting
	vec3 viewDir = normalize(cameraPos - fragPosition);
	vec3 halfDir = normalize(lightDir + viewDir);
	int exp = 8;
	
	//float amp = lightIntensity / length(lightDir);

	float specAngle = max(dot(halfDir, normals), 0.0);
	float specular = pow(specAngle, exp);

	vec4 result = ambient + vec4(diffuse,1)*f + (specular * vec4(1, 1, 1,1));
	fcolor = result * f;
	//float w = depthPosition.w;
	//fcolor = vec4(depthPosition.x/w,depthPosition.y/w,0,1);

	
	//fcolor = texture(normalMap,texCoord);
	
}


