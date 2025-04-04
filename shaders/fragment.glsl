#version 330 core
out vec4 FragColor;
uniform vec2 u_res;

void main() {
    vec2 uv = (2.0 * gl_FragCoord.xy - u_res.xy) / u_res.y;
    
    float d = length(uv) - 0.5;
    FragColor = vec4(vec3(1.0 - smoothstep(0.0, 0.02, d)), 1.0);
}