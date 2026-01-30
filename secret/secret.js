const canvas = document.getElementById("gl");
const gl = canvas.getContext("webgl", {antialias: false});

function resize() {
    canvas.width = innerWidth;
    canvas.height = innerHeight;
    gl.viewport(0, 0, canvas.width, canvas.height);
}
addEventListener("resize", resize);
resize();

/* ===== Shaders ===== */

const vert = `
attribute vec2 position;
varying vec2 vUv;
void main() {
  vUv = position * 0.5 + 0.5;
  gl_Position = vec4(position, 0.0, 1.0);
}
`;

const frag = `
precision highp float;
varying vec2 vUv;

uniform float time;
uniform vec2 drops[16];
uniform float power[16];

void main() {
  vec2 uv = vUv;
  vec2 warped = uv;

  for (int i = 0; i < 16; i++) {
    vec2 d = warped - drops[i];
    float dist = length(d);
    float wave = sin(dist * 50.0 - time * 5.0);
    float decay = exp(-dist * 8.0);
    warped += normalize(d) * wave * decay * power[i] * 0.015;
  }

  float vignette = smoothstep(0.8, 0.2, length(warped - 0.5));
  vec3 color = vec3(0.44, 0.4, 0.88) * vignette;

  gl_FragColor = vec4(color, 1.0);
}
`;

/* ===== Compile ===== */

function shader(type, src) {
    const s = gl.createShader(type);
    gl.shaderSource(s, src);
    gl.compileShader(s);
    return s;
}

const prog = gl.createProgram();
gl.attachShader(prog, shader(gl.VERTEX_SHADER, vert));
gl.attachShader(prog, shader(gl.FRAGMENT_SHADER, frag));
gl.linkProgram(prog);
gl.useProgram(prog);

/* ===== Geometry ===== */

const quad = gl.createBuffer();
gl.bindBuffer(gl.ARRAY_BUFFER, quad);
gl.bufferData(
    gl.ARRAY_BUFFER,
    new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]),
    gl.STATIC_DRAW
);

const pos = gl.getAttribLocation(prog, "position");
gl.enableVertexAttribArray(pos);
gl.vertexAttribPointer(pos, 2, gl.FLOAT, false, 0, 0);

/* ===== Uniforms ===== */

const timeLoc = gl.getUniformLocation(prog, "time");
const dropsLoc = gl.getUniformLocation(prog, "drops");
const powerLoc = gl.getUniformLocation(prog, "power");

/* ===== Ripple data ===== */

const MAX = 16;
let drops = Array(MAX).fill([10, 10]);
let power = Array(MAX).fill(0);
let ptr = 0;

addEventListener("pointermove", e => {
    drops[ptr] = [
        e.clientX / canvas.width,
        1.0 - e.clientY / canvas.height
    ];
    power[ptr] = 1.0;
    ptr = (ptr + 1) % MAX;
});

/* ===== Render loop ===== */

let t = 0;
function loop() {
    t += 0.016;
    power = power.map(p => p * 0.95);

    gl.uniform1f(timeLoc, t);
    gl.uniform2fv(dropsLoc, drops.flat());
    gl.uniform1fv(powerLoc, power);

    gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
    requestAnimationFrame(loop);
}

loop();
