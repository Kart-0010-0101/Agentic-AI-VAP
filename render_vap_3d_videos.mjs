/**
 * Render 6 deterministic procedural 3D explainer videos (14-16s, 1280x720, 30 fps)
 * using Three.js + headless Chrome WebGL2 (puppeteer-core) + ffmpeg pipe.
 * Aesthetic: Pure-white (#FFFFFF) architectural studio (taste-skill) with
 * surface-printed 3D block labels on every pedestal & cube.
 */

import fs from "node:fs";
import http from "node:http";
import path from "node:path";
import { spawn } from "node:child_process";
import { createRequire } from "node:module";

const TEMP_ENV = path.join(process.env.TEMP || "C:\\Temp", "vap_three_render");
const require = createRequire(path.join(TEMP_ENV, "package.json"));
const puppeteer = require("puppeteer-core");

const VAP_DIR = "C:\\Users\\lapto\\Desktop\\demo\\BEN\\VAP";
const VIDEOS_DIR = path.join(VAP_DIR, "videos");
fs.mkdirSync(VIDEOS_DIR, { recursive: true });

const THREE_DIR = path.join(TEMP_ENV, "node_modules", "three", "build");
const CHROME_PATH = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";

const W = 1280;
const H = 720;
const FPS = 30;

const SCENES = [
  { name: "anim_closed_loop", duration: 15.0, posterT: 10.5, subtitle: "DAY 1  //  OPEN-LOOP VS CLOSED-LOOP CONTROL" },
  { name: "anim_cosine_search", duration: 14.0, posterT: 10.2, subtitle: "DAY 1  //  3D COSINE VECTOR ALIGNMENT" },
  { name: "anim_chunking_window", duration: 14.0, posterT: 8.4, subtitle: "DAY 2  //  SLIDING WINDOW CHUNKING -> HNSW" },
  { name: "anim_react_self_heal", duration: 16.0, posterT: 11.5, subtitle: "DAY 3  //  REACT SELF-HEALING EXECUTION LOOP" },
  { name: "anim_cross_session_memory", duration: 16.0, posterT: 15.2, subtitle: "DAY 3  //  CROSS-SESSION EPISODIC MEMORY" },
  { name: "anim_fault_recovery", duration: 15.0, posterT: 9.5, subtitle: "DAY 5  //  SANDBOX FAULT ISOLATION & RECOVERY" },
  { name: "anim_rag_pipeline", duration: 15.0, posterT: 10.0, subtitle: "DAY 1  //  RAG RETRIEVAL-AUGMENTED GENERATION" },
];

const HTML_TEMPLATE = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  html, body { width: 1280px; height: 720px; overflow: hidden; background: #FFFFFF; font-family: "Segoe UI", system-ui, sans-serif; }
  #stage { position: fixed; inset: 0; width: 1280px; height: 720px; display: block; }
  .hud-pill {
    position: fixed; top: 24px; left: 28px;
    display: inline-flex; align-items: center; gap: 10px;
    padding: 8px 14px; background: rgba(255,255,255,0.96);
    border: 1px solid #E2E8F0; border-radius: 999px;
    box-shadow: 0 2px 10px rgba(15,23,42,0.05);
  }
  .hud-dot { width: 8px; height: 8px; border-radius: 50%; background: #EA580C; }
  .hud-phase {
    font-family: "Consolas", monospace; font-size: 12px; font-weight: 700;
    letter-spacing: 0.08em; color: #0F172A; text-transform: uppercase;
  }
  .hud-meta {
    position: fixed; top: 28px; right: 28px;
    font-family: "Consolas", monospace; font-size: 11px; font-weight: 700;
    letter-spacing: 0.08em; color: #64748B; text-transform: uppercase;
  }
  .hud-bar-bg {
    position: fixed; left: 0; right: 0; bottom: 0; height: 4px; background: #E2E8F0;
  }
  .hud-bar-fill {
    height: 100%; width: 0%; background: #EA580C;
  }
</style>
</head>
<body>
  <canvas id="stage" width="1280" height="720"></canvas>
  <div class="hud-pill"><span class="hud-dot" id="hudDot"></span><span class="hud-phase" id="hudPhase">INITIALIZING</span></div>
  <div class="hud-meta" id="hudMeta">VAP ARCHITECTURAL 3D</div>
  <div class="hud-bar-bg"><div class="hud-bar-fill" id="hudBar"></div></div>

  <script type="importmap">
  { "imports": { "three": "/three.module.js" } }
  </script>
  <script type="module">
    import * as THREE from "three";

    const PAL = {
      white: 0xffffff,
      floor: 0xf8fafc,
      slateDark: 0x0f172a,
      slateMed: 0x475569,
      hairline: 0xcbd5e1,
      blue: 0x1e3a8a,
      blueLt: 0x3b82f6,
      orange: 0xea580c,
      amber: 0xf59e0b,
      green: 0x15803d,
      red: 0xb91c1c,
    };

    function clamp01(v) { return Math.max(0, Math.min(1, v)); }
    function smoothstep(a, b, x) {
      const u = clamp01((x - a) / Math.max(1e-6, b - a));
      return u * u * (3 - 2 * u);
    }
    function lerp(a, b, t) { return a + (b - a) * clamp01(t); }
    function toCssHex(num) { return "#" + num.toString(16).padStart(6, "0"); }

    const canvas = document.getElementById("stage");
    const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true });
    renderer.setSize(1280, 720, false);
    renderer.setPixelRatio(1);
    renderer.setClearColor(0xffffff, 1);
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.05;

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xffffff);
    scene.fog = new THREE.Fog(0xffffff, 30, 64);

    const camera = new THREE.PerspectiveCamera(38, 1280 / 720, 0.1, 120);

    const hemi = new THREE.HemisphereLight(0xffffff, 0xe2e8f0, 1.45);
    scene.add(hemi);
    const keyLight = new THREE.DirectionalLight(0xffffff, 1.25);
    keyLight.position.set(10, 18, 12);
    keyLight.castShadow = true;
    keyLight.shadow.mapSize.set(2048, 2048);
    keyLight.shadow.camera.left = -16;
    keyLight.shadow.camera.right = 16;
    keyLight.shadow.camera.top = 14;
    keyLight.shadow.camera.bottom = -14;
    keyLight.shadow.camera.near = 1;
    keyLight.shadow.camera.far = 45;
    keyLight.shadow.bias = -0.0005;
    scene.add(keyLight);

    const rimLight = new THREE.DirectionalLight(0xe0e7ff, 0.45);
    rimLight.position.set(-12, 8, -10);
    scene.add(rimLight);

    const shadowFloor = new THREE.Mesh(
      new THREE.PlaneGeometry(80, 80),
      new THREE.ShadowMaterial({ opacity: 0.08 })
    );
    shadowFloor.rotation.x = -Math.PI / 2;
    shadowFloor.receiveShadow = true;
    scene.add(shadowFloor);

    const grid = new THREE.GridHelper(36, 36, 0xcbd5e1, 0xf1f5f9);
    grid.position.y = 0.002;
    scene.add(grid);

    function makeCardSprite(title, sub = "", borderHex = "#1E3A8A", bgHex = "#FFFFFF", scaleW = 3.2, y = 2.6) {
      const c = document.createElement("canvas");
      c.width = 640; c.height = 176;
      const ctx = c.getContext("2d");
      ctx.fillStyle = bgHex;
      ctx.beginPath();
      ctx.roundRect(10, 10, 620, 156, 18);
      ctx.fill();
      ctx.lineWidth = 5;
      ctx.strokeStyle = borderHex;
      ctx.stroke();

      ctx.fillStyle = "#0F172A";
      ctx.font = "700 32px 'Segoe UI', system-ui, sans-serif";
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      ctx.fillText(title, 320, sub ? 66 : 88, 576);

      if (sub) {
        ctx.fillStyle = borderHex;
        ctx.font = "700 23px 'Consolas', monospace";
        ctx.fillText(sub, 320, 118, 576);
      }

      const tex = new THREE.CanvasTexture(c);
      tex.colorSpace = THREE.SRGBColorSpace;
      const mat = new THREE.SpriteMaterial({ map: tex, transparent: true, depthTest: false, toneMapped: false });
      const sp = new THREE.Sprite(mat);
      sp.scale.set(scaleW, scaleW * (176 / 640), 1);
      sp.position.y = y;
      return sp;
    }

    function makeFaceLabelTexture(title, sub = "", bgHex = "#FFFFFF", accentHex = "#1E3A8A", inkHex = "#0F172A") {
      const c = document.createElement("canvas");
      c.width = 512; c.height = 320;
      const ctx = c.getContext("2d");
      ctx.fillStyle = bgHex;
      ctx.fillRect(0, 0, 512, 320);

      // Clean accent stripe on top of face
      ctx.fillStyle = accentHex;
      ctx.fillRect(0, 0, 512, 30);

      ctx.fillStyle = inkHex;
      ctx.font = "800 54px 'Segoe UI', system-ui, sans-serif";
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      ctx.fillText(title, 256, sub ? 142 : 172, 464);

      if (sub) {
        ctx.fillStyle = accentHex;
        ctx.font = "700 30px 'Consolas', monospace";
        ctx.fillText(sub, 256, 224, 464);
      }

      const tex = new THREE.CanvasTexture(c);
      tex.colorSpace = THREE.SRGBColorSpace;
      return tex;
    }

    function makeScreenBoard(w, h, drawFn) {
      const c = document.createElement("canvas");
      c.width = 768; c.height = Math.round(768 * (h / w));
      const ctx = c.getContext("2d");
      const tex = new THREE.CanvasTexture(c);
      tex.colorSpace = THREE.SRGBColorSpace;
      const mat = new THREE.MeshBasicMaterial({ map: tex, toneMapped: false });
      const mesh = new THREE.Mesh(new THREE.PlaneGeometry(w, h), mat);
      const frame = new THREE.Mesh(
        new THREE.BoxGeometry(w + 0.14, h + 0.14, 0.08),
        new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.4, metalness: 0.2 })
      );
      frame.position.z = -0.045;
      frame.castShadow = true;
      const grp = new THREE.Group();
      grp.add(frame);
      grp.add(mesh);
      grp.userData.update = (arg) => {
        drawFn(ctx, c.width, c.height, arg);
        tex.needsUpdate = true;
      };
      return grp;
    }

    /**
     * Create architectural block with crisp surface-printed labels on Top (+Y) & Front (+Z) faces.
     * BoxGeometry face order: 0:+X, 1:-X, 2:+Y(top), 3:-Y, 4:+Z(front), 5:-Z
     */
    function addPedestal(parent, x, z, w, h, d, color = 0xffffff, edgeColor = 0xcbd5e1, label = "", sub = "", customHex = null) {
      const sideMat = new THREE.MeshStandardMaterial({ color, roughness: 0.40, metalness: 0.06 });
      let matArg = sideMat;
      if (label) {
        const bgHex = toCssHex(color);
        const accentHex = customHex || toCssHex(edgeColor);
        const tex = makeFaceLabelTexture(label, sub, bgHex, accentHex);
        const labelMat = new THREE.MeshStandardMaterial({ map: tex, roughness: 0.35, metalness: 0.04 });
        matArg = [sideMat, sideMat, labelMat, sideMat, labelMat, sideMat];
      }
      const mesh = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), matArg);
      mesh.position.set(x, h / 2, z);
      mesh.castShadow = true;
      mesh.receiveShadow = true;
      parent.add(mesh);
      const edges = new THREE.LineSegments(
        new THREE.EdgesGeometry(new THREE.BoxGeometry(w, h, d)),
        new THREE.LineBasicMaterial({ color: edgeColor })
      );
      mesh.add(edges);
      return mesh;
    }

    function addLabeledCube(parent, size, bgColor, edgeColor, label, sub = "") {
      const bgHex = toCssHex(bgColor);
      const accHex = toCssHex(edgeColor);
      const tex = makeFaceLabelTexture(label, sub, bgHex, accHex, bgColor === 0xffffff ? "#0F172A" : "#FFFFFF");
      const faceMat = new THREE.MeshStandardMaterial({ map: tex, roughness: 0.28, metalness: 0.05 });
      const mesh = new THREE.Mesh(
        new THREE.BoxGeometry(size, size, size),
        [faceMat, faceMat, faceMat, faceMat, faceMat, faceMat]
      );
      mesh.castShadow = true;
      parent.add(mesh);
      return mesh;
    }

    function addTubePath(parent, points, radius = 0.06, color = 0x1e3a8a, opacity = 0.78) {
      const curve = new THREE.CatmullRomCurve3(points.map(p => new THREE.Vector3(...p)));
      const tube = new THREE.Mesh(
        new THREE.TubeGeometry(curve, 64, radius, 12, false),
        new THREE.MeshStandardMaterial({
          color, roughness: 0.28, metalness: 0.15,
          transparent: opacity < 1, opacity
        })
      );
      tube.castShadow = true;
      parent.add(tube);
      return curve;
    }

    function setHud(phase, pct, color = "#EA580C") {
      document.getElementById("hudPhase").textContent = phase;
      document.getElementById("hudDot").style.background = color;
      const bar = document.getElementById("hudBar");
      bar.style.width = (clamp01(pct) * 100).toFixed(2) + "%";
      bar.style.background = color;
    }

    let activeUpdate = () => {};

    window.initScene = function(sceneName, subtitleText, totalDuration) {
      document.getElementById("hudMeta").textContent = subtitleText;

      for (let i = scene.children.length - 1; i >= 0; i--) {
        const ch = scene.children[i];
        if (!ch.isLight && ch !== shadowFloor && ch !== grid) scene.remove(ch);
      }

      const root = new THREE.Group();
      scene.add(root);

      const pos = new THREE.Vector3();
      const look = new THREE.Vector3();

      // =========================================================================
      // SCENE 1: anim_closed_loop (All 7 pedestals labeled + dynamic status)
      // =========================================================================
      if (sceneName === "anim_closed_loop") {
        addPedestal(root, -4.4, 0, 6.2, 0.24, 3.8, 0xf8fafc, 0xcbd5e1);
        addPedestal(root, -6.3, 0, 1.35, 0.95, 1.35, 0xffffff, 0x1e3a8a, "INPUT", "Prompt");
        addPedestal(root, -4.4, 0, 1.45, 1.05, 1.35, 0xffffff, 0x1e3a8a, "LLM", "Script");
        const olGate = addPedestal(root, -2.4, 0, 1.35, 1.45, 1.65, 0xfef2f2, 0xb91c1c, "FAULT", "JSON Err");
        addTubePath(root, [[-6.3, 0.78, 0], [-2.4, 0.78, 0]], 0.07, 0xcbd5e1, 0.9);

        const olBadge = makeCardSprite("OPEN-LOOP SCRIPT", "Zero Feedback", "#B91C1C", "#FFFFFF", 3.3, 2.8);
        olBadge.position.set(-4.4, 2.8, -0.5);
        root.add(olBadge);

        const olFaultBadge = makeCardSprite("JSON FAULT GATE", "HALTED", "#B91C1C", "#FEF2F2", 2.7, 2.35);
        olFaultBadge.position.set(-2.4, 2.35, 0.8);
        root.add(olFaultBadge);

        const olPacket = addLabeledCube(root, 0.56, 0x3b82f6, 0x1e3a8a, "REQ", "Data");

        const clDisc = new THREE.Mesh(
          new THREE.CylinderGeometry(3.3, 3.45, 0.26, 48),
          new THREE.MeshStandardMaterial({ color: 0xf8fafc, roughness: 0.45 })
        );
        clDisc.position.set(4.4, 0.13, 0);
        clDisc.receiveShadow = true;
        root.add(clDisc);

        const ringTrack = new THREE.Mesh(
          new THREE.TorusGeometry(2.15, 0.06, 14, 64),
          new THREE.MeshStandardMaterial({ color: 0x1e3a8a, roughness: 0.3 })
        );
        ringTrack.rotation.x = Math.PI / 2;
        ringTrack.position.set(4.4, 0.85, 0);
        root.add(ringTrack);

        const nodeCoords = [
          { x: 4.4, z: -2.15, lbl: "PLANNER", sub: "LLM", col: 0x1e3a8a },
          { x: 6.55, z: 0.0, lbl: "TOOL", sub: "Python", col: 0xea580c },
          { x: 4.4, z: 2.15, lbl: "OBSERVE", sub: "Sensor", col: 0x15803d },
          { x: 2.25, z: 0.0, lbl: "MEMORY", sub: "Self-Heal", col: 0x15803d },
        ];
        nodeCoords.forEach((n) => {
          addPedestal(root, n.x, n.z, 1.32, 0.96, 1.25, 0xffffff, n.col, n.lbl, n.sub);
        });

        const clBadge = makeCardSprite("CLOSED-LOOP REACT", "Self-Healing Ring", "#15803D", "#FFFFFF", 3.5, 3.05);
        clBadge.position.set(4.4, 3.05, 0);
        root.add(clBadge);

        const clPacket = addLabeledCube(root, 0.56, 0xea580c, 0xffffff, "TASK", "Loop");

        const bypassCurve = addTubePath(root, [
          [4.4, 0.9, 2.15], [3.2, 2.05, 1.3], [2.25, 0.9, 0.0]
        ], 0.055, PAL.green, 0.88);

        activeUpdate = (t) => {
          const p = clamp01(t / totalDuration);

          const olMove = smoothstep(0.05, 0.35, p);
          olPacket.position.set(lerp(-6.3, -3.35, olMove), 1.25, 0);
          olPacket.rotation.y = olMove * Math.PI;
          const crashed = p > 0.35;
          olFaultBadge.visible = crashed;

          const clAngle = lerp(-Math.PI / 2, Math.PI * 1.5, smoothstep(0.15, 0.92, p));
          if (p > 0.56 && p < 0.74) {
            const bu = smoothstep(0.56, 0.74, p);
            clPacket.position.copy(bypassCurve.getPoint(bu));
            clPacket.position.y += 0.25;
          } else {
            clPacket.position.set(4.4 + Math.cos(clAngle) * 2.15, 1.26, Math.sin(clAngle) * 2.15);
          }
          clPacket.rotation.y = t * 1.2;

          if (p < 0.22) {
            const u = smoothstep(0.0, 0.22, p);
            pos.set(0, lerp(11.5, 8.6, u), lerp(18.0, 14.5, u));
            look.set(0, 1.2, 0);
            setHud("1 / 4  COMPARING CONTROL ARCHITECTURES", p, "#1E3A8A");
          } else if (p < 0.48) {
            const u = smoothstep(0.22, 0.32, p);
            pos.set(lerp(0, -4.4, u), lerp(8.6, 5.4, u), lerp(14.5, 9.0, u));
            look.set(lerp(0, -4.2, u), 1.2, 0);
            const shake = Math.exp(-Math.pow((p - 0.36) * 20, 2)) * 0.22;
            pos.x += Math.sin(t * 58) * shake;
            pos.y += Math.cos(t * 49) * shake;
            setHud(p > 0.35 ? "2 / 4  OPEN-LOOP CRASHED AT FAULT GATE" : "2 / 4  OPEN-LOOP EXECUTING", p, "#B91C1C");
          } else if (p < 0.80) {
            const u = smoothstep(0.48, 0.60, p);
            pos.set(lerp(-4.4, 4.4, u), 5.6, lerp(9.0, 9.0, u));
            look.set(lerp(-4.2, 4.4, u), 1.1, 0);
            setHud(p > 0.65 ? "3 / 4  DETOUR VIA MEMORY -> SELF-HEAL" : "3 / 4  DETECTING OBSERVATION ERROR", p, "#EA580C");
          } else {
            const u = smoothstep(0.80, 1.0, p);
            pos.set(lerp(4.4, 1.4, u), lerp(5.6, 8.2, u), lerp(9.0, 14.2, u));
            look.set(lerp(4.4, 1.0, u), 1.2, 0);
            setHud("4 / 4  CLOSED-LOOP CONVERGED ON FINAL ANSWER", p, "#15803D");
          }
          camera.position.copy(pos);
          camera.lookAt(look);
        };
      }

      // =========================================================================
      // SCENE 2: anim_cosine_search (No sprite collisions + labeled origin block)
      // =========================================================================
      else if (sceneName === "anim_cosine_search") {
        addPedestal(root, 0, 0, 1.8, 0.42, 1.8, 0xffffff, 0x0f172a, "VECTOR", "ORIGIN");

        for (const rot of [[0,0,0], [Math.PI/2,0,0], [0,Math.PI/2,0]]) {
          const rg = new THREE.TorusGeometry(4.2, 0.015, 8, 72);
          const rm = new THREE.Mesh(rg, new THREE.MeshBasicMaterial({ color: 0xe2e8f0 }));
          rm.rotation.set(...rot);
          rm.position.y = 0.45;
          root.add(rm);
        }

        const origin = new THREE.Vector3(0, 0.45, 0);
        const vecDefs = [
          { dir: new THREE.Vector3(0.75, 0.56, 0.34).normalize(), len: 4.1, col: PAL.green, lbl: "DOC A: MOSFET", sub: "55V / 100V Spec" },
          { dir: new THREE.Vector3(-0.82, 0.40, 0.40).normalize(), len: 3.9, col: PAL.blue, lbl: "DOC B: WI-FI 6E", sub: "2.4 / 5 GHz" },
          { dir: new THREE.Vector3(-0.25, 0.38, -0.89).normalize(), len: 3.9, col: PAL.slateMed, lbl: "DOC C: 5G PRB", sub: "NR Telemetry" },
        ];
        vecDefs.forEach((v) => {
          const ah = new THREE.ArrowHelper(v.dir, origin, v.len, v.col, 0.45, 0.24);
          root.add(ah);
          const tip = origin.clone().addScaledVector(v.dir, v.len + 0.45);
          const sp = makeCardSprite(v.lbl, v.sub, toCssHex(v.col), "#FFFFFF", 2.45, 2.0);
          sp.position.set(tip.x, Math.min(2.6, Math.max(1.5, tip.y - 0.15)), tip.z);
          root.add(sp);
        });

        const qDir = new THREE.Vector3(-0.35, 0.72, 0.59).normalize();
        const qArrow = new THREE.ArrowHelper(qDir, origin, 4.3, PAL.orange, 0.48, 0.26);
        root.add(qArrow);
        // Offset higher so USER QUERY sits strictly above DOC A badge
        const qSprite = makeCardSprite("USER QUERY", "max Vds?", "#EA580C", "#FFF7ED", 2.35, 3.6);
        root.add(qSprite);

        // Live 3D Readout Board offset cleanly to far right foreground
        const board = makeScreenBoard(3.8, 1.9, (ctx, w, h, data) => {
          ctx.fillStyle = "#FFFFFF";
          ctx.fillRect(0, 0, w, h);
          ctx.strokeStyle = "#EA580C";
          ctx.lineWidth = 8;
          ctx.strokeRect(4, 4, w - 8, h - 8);
          ctx.fillStyle = "#64748B";
          ctx.font = "700 23px Consolas, monospace";
          ctx.fillText("LIVE COSINE METRIC (CHROMA HNSW)", 30, 50);
          ctx.fillStyle = "#0F172A";
          ctx.font = "700 54px 'Segoe UI', sans-serif";
          ctx.fillText("cos(\u03B8) = " + data.cos.toFixed(2), 30, 150);
          ctx.fillStyle = data.cos > 0.85 ? "#15803D" : "#EA580C";
          ctx.font = "700 31px Consolas, monospace";
          ctx.fillText("\u03B8 = " + data.deg.toFixed(1) + "\u00B0  |  " + (data.cos > 0.85 ? "MATCH LOCKED" : "SCANNING..."), 30, 238);
        });
        board.position.set(6.55, 2.05, 1.35);
        board.rotation.y = -0.52;
        root.add(board);

        const targetDir = vecDefs[0].dir;
        const startDir = new THREE.Vector3(-0.35, 0.72, 0.59).normalize();

        activeUpdate = (t) => {
          const p = clamp01(t / totalDuration);
          const align = smoothstep(0.16, 0.74, p);
          const cur = new THREE.Vector3().lerpVectors(startDir, targetDir.clone().add(new THREE.Vector3(0.05, 0.14, 0.05)), align).normalize();
          qArrow.setDirection(cur);

          const dot = clamp01(cur.dot(targetDir));
          const deg = Math.acos(Math.min(1, dot)) * (180 / Math.PI);
          board.userData.update({ cos: dot, deg });

          const tip = origin.clone().addScaledVector(cur, 4.4);
          qSprite.position.set(tip.x - 0.1, Math.min(3.9, Math.max(3.15, tip.y + 0.9)), tip.z);

          const ang = lerp(-0.48, 0.42, smoothstep(0.10, 0.85, p));
          const rad = lerp(14.5, 11.2, smoothstep(0.55, 1.0, p));
          pos.set(Math.sin(ang) * rad, lerp(7.6, 5.2, p), Math.cos(ang) * rad);
          look.set(lerp(1.0, 2.3, smoothstep(0.55, 1.0, p)), 1.9, 0.1);
          camera.position.copy(pos);
          camera.lookAt(look);
          setHud(dot > 0.88 ? "3 / 3  HIGH SIMILARITY LOCKED (TOP-K #1)" : "2 / 3  ALIGNING QUERY IN 384-D VECTOR SPACE", p, dot > 0.88 ? "#15803D" : "#EA580C");
        };
      }

      // =========================================================================
      // SCENE 3: anim_chunking_window (Every slab & HNSW tier labeled)
      // =========================================================================
      else if (sceneName === "anim_chunking_window") {
        const slabs = [];
        for (let i = 0; i < 6; i++) {
          const sx = -5.8 + i * 1.45;
          const slab = addPedestal(root, sx, 0.6, 1.25, 1.8, 0.62, 0xffffff, 0x1e3a8a, "SENT " + (i + 1), "Chunk " + (i + 1));
          slabs.push({ mesh: slab, x: sx });
        }

        const bracket = new THREE.Group();
        const bBox = new THREE.Mesh(
          new THREE.BoxGeometry(3.05, 2.2, 0.92),
          new THREE.MeshStandardMaterial({ color: PAL.orange, transparent: true, opacity: 0.18, roughness: 0.2 })
        );
        const bEdges = new THREE.LineSegments(
          new THREE.EdgesGeometry(new THREE.BoxGeometry(3.05, 2.2, 0.92)),
          new THREE.LineBasicMaterial({ color: PAL.orange })
        );
        bracket.add(bBox, bEdges);
        bracket.position.set(-5.0, 1.0, 0.6);
        root.add(bracket);

        const winBadge = makeCardSprite("SLIDING WINDOW", "500 chars / 50 overlap", "#EA580C", "#FFF7ED", 3.2, 3.15);
        root.add(winBadge);

        const tiers = [
          { y: 0.22, lbl: "HNSW L0", sub: "All Nodes", w: 3.1, d: 2.5 },
          { y: 1.38, lbl: "HNSW L1", sub: "Hubs", w: 2.7, d: 2.1 },
          { y: 2.54, lbl: "HNSW L2", sub: "Entry", w: 2.3, d: 1.8 },
        ];
        tiers.forEach((tr) => {
          const disc = addPedestal(root, 4.9, 0.0, tr.w, 0.36, tr.d, 0xf8fafc, 0x1e3a8a, tr.lbl, tr.sub);
          disc.position.y = tr.y;
        });
        const hnswBadge = makeCardSprite("CHROMA HNSW INDEX", "Idempotent upsert()", "#1E3A8A", "#FFFFFF", 3.2, 3.65);
        hnswBadge.position.set(4.9, 3.65, 0);
        root.add(hnswBadge);

        const prisms = [0, 1, 2].map((i) =>
          addLabeledCube(root, 0.56, i === 1 ? PAL.green : PAL.blueLt, 0xffffff, "VEC " + (i + 1), "384d")
        );

        activeUpdate = (t) => {
          const p = clamp01(t / totalDuration);
          const slide = smoothstep(0.12, 0.72, p);
          const bx = lerp(-5.1, 0.7, slide);
          bracket.position.x = bx;
          winBadge.position.set(bx, 3.15, 0.6);

          slabs.forEach((s) => {
            const dist = Math.abs(s.x - bx);
            const inside = dist < 1.55;
            s.mesh.position.y = inside ? 1.05 : 0.9;
          });

          prisms.forEach((pr, idx) => {
            const start = 0.25 + idx * 0.18;
            const u = smoothstep(start, start + 0.22, p);
            const sx = lerp(-4.5 + idx * 2.2, 4.9 + (idx - 1) * 0.55, u);
            const sy = lerp(1.6, tiers[idx].y + 0.52, u) + Math.sin(u * Math.PI) * 2.2;
            pr.position.set(sx, sy, lerp(0.6, 0.0, u));
            pr.rotation.y = t * 1.4 + idx;
            pr.visible = p > start;
          });

          if (p < 0.20) {
            const u = smoothstep(0, 0.20, p);
            pos.set(-0.5, lerp(10.5, 7.2, u), lerp(16.5, 13.0, u));
            look.set(-0.5, 1.5, 0.2);
            setHud("1 / 3  SENTENCE STREAM OVERVIEW", p, "#1E3A8A");
          } else if (p < 0.68) {
            const u = smoothstep(0.20, 0.68, p);
            pos.set(lerp(-4.8, 0.8, u), 5.2, 9.8);
            look.set(lerp(-4.8, 0.8, u), 1.4, 0.4);
            setHud("2 / 3  EXTRUDING OVERLAPPED CHUNKS", p, "#EA580C");
          } else {
            const u = smoothstep(0.68, 1.0, p);
            pos.set(lerp(0.8, 5.2, u), lerp(5.2, 5.8, u), lerp(9.8, 9.0, u));
            look.set(lerp(0.8, 4.8, u), 1.9, 0);
            setHud("3 / 3  EMBEDDING INTO CHROMA HNSW TOWER", p, "#15803D");
          }
          camera.position.copy(pos);
          camera.lookAt(look);
        };
      }

      // =========================================================================
      // SCENE 4: anim_react_self_heal (Labeled stations + labeled packet)
      // =========================================================================
      else if (sceneName === "anim_react_self_heal") {
        addPedestal(root, -5.2, 0.2, 2.3, 1.35, 1.8, 0xffffff, 0x1e3a8a, "PLANNER", "Step Loop");
        addPedestal(root, 0.0, 0.2, 2.3, 1.35, 1.8, 0xffffff, 0xea580c, "TOOL CALL", "tools.py");
        addPedestal(root, 5.2, 0.2, 2.3, 1.35, 1.8, 0xffffff, 0x15803d, "SYNTHESIS", "Report");

        const sp1 = makeCardSprite("1. LLM PLANNER", "Reasoning", "#1E3A8A", "#FFFFFF", 2.9, 2.45);
        sp1.position.x = -5.2;
        const sp2 = makeCardSprite("2. PYTHON TOOL", "Execution", "#EA580C", "#FFFFFF", 2.9, 2.45);
        const sp3 = makeCardSprite("3. FINAL ANSWER", "Verified", "#15803D", "#FFFFFF", 2.9, 2.45);
        sp3.position.x = 5.2;
        root.add(sp1, sp2, sp3);

        const pipe1 = addTubePath(root, [[-4.1, 0.9, 0.2], [0.0, 0.9, 0.2]], 0.07, 0x94a3b8, 0.85);
        const bypass = addTubePath(root, [[-4.1, 0.9, -0.3], [-2.0, 2.2, -1.0], [0.0, 0.9, -0.3]], 0.06, 0x15803d, 0.85);
        const pipe2 = addTubePath(root, [[1.1, 0.9, 0.2], [5.2, 0.9, 0.2]], 0.07, 0x15803d, 0.85);

        const term = makeScreenBoard(6.4, 2.1, (ctx, w, h, p) => {
          ctx.fillStyle = "#0B1220";
          ctx.fillRect(0, 0, w, h);
          ctx.fillStyle = "#1E293B";
          ctx.fillRect(0, 0, w, 40);
          ctx.fillStyle = "#E2E8F0";
          ctx.font = "700 18px Consolas, monospace";
          ctx.fillText("LIVE REACT AGENT TRACE  //  trace.jsonl", 18, 26);

          const lines = [
            { t: 0.05, c: "#60A5FA", txt: "[STEP 1] ACTION: read_file('sensor.csv')" },
            { t: 0.28, c: "#F87171", txt: "[OBS 1]  ERR: FileNotFoundError -> Hints: ['data/']" },
            { t: 0.50, c: "#FBBF24", txt: "[STEP 2] THOUGHT: Inspect data/ -> list_dir('data')" },
            { t: 0.68, c: "#4ADE80", txt: "[OBS 2]  RECOVERED: Found 'data/iot_log.json' (124 rows)" },
            { t: 0.82, c: "#4ADE80", txt: "[FINAL]  Anomaly report generated cleanly (0 crashes)" },
          ];
          let y = 78;
          lines.forEach((ln) => {
            if (p >= ln.t) {
              ctx.fillStyle = ln.c;
              ctx.font = "700 20px Consolas, monospace";
              ctx.fillText(ln.txt, 18, y);
              y += 32;
            }
          });
        });
        term.position.set(0, 3.45, -2.5);
        root.add(term);

        const pkt = addLabeledCube(root, 0.54, 0xea580c, 0xffffff, "JSON", "Call");

        activeUpdate = (t) => {
          const p = clamp01(t / totalDuration);
          term.userData.update(p);
          pkt.rotation.y = t * 1.4;

          if (p < 0.30) {
            pkt.position.copy(pipe1.getPoint(smoothstep(0.05, 0.30, p)));
          } else if (p < 0.52) {
            pkt.position.copy(pipe1.getPoint(1 - smoothstep(0.34, 0.52, p)));
          } else if (p < 0.72) {
            pkt.position.copy(bypass.getPoint(smoothstep(0.54, 0.72, p)));
          } else {
            pkt.position.copy(pipe2.getPoint(smoothstep(0.72, 0.92, p)));
          }
          pkt.position.y += 0.3;

          if (p < 0.18) {
            const u = smoothstep(0, 0.18, p);
            pos.set(0, lerp(9.5, 6.4, u), lerp(16.5, 12.6, u));
            look.set(0, 1.8, -0.5);
            setHud("1 / 4  DISPATCHING INITIAL TOOL ACTION", p, "#1E3A8A");
          } else if (p < 0.45) {
            const u = smoothstep(0.18, 0.30, p);
            pos.set(lerp(0, 0.3, u), lerp(6.4, 4.8, u), lerp(12.6, 7.8, u));
            look.set(0, 1.8, -0.4);
            const shake = Math.exp(-Math.pow((p - 0.31) * 20, 2)) * 0.24;
            pos.x += Math.sin(t * 55) * shake;
            pos.y += Math.cos(t * 48) * shake;
            setHud(p > 0.29 ? "2 / 4  CAUGHT FILENOTFOUNDERROR WITHOUT CRASH" : "2 / 4  EXECUTING PYTHON TOOL", p, "#B91C1C");
          } else if (p < 0.68) {
            const u = smoothstep(0.45, 0.56, p);
            pos.set(lerp(0.3, -4.8, u), 4.9, lerp(7.8, 8.4, u));
            look.set(lerp(0, -4.4, u), 1.8, -0.2);
            setHud("3 / 4  LLM REFLECTS & REROUTES PATH", p, "#EA580C");
          } else {
            const u = smoothstep(0.68, 0.85, p);
            pos.set(lerp(-4.8, 3.4, u), lerp(4.9, 5.4, u), lerp(8.4, 10.8, u));
            look.set(lerp(-4.4, 2.5, u), 1.9, -0.6);
            setHud("4 / 4  SELF-HEALING COMPLETE -> FINAL ANSWER", p, "#15803D");
          }
          camera.position.copy(pos);
          camera.lookAt(look);
        };
      }

      // =========================================================================
      // SCENE 5: anim_cross_session_memory (Steps 1-4 & Recall/Solved labeled)
      // =========================================================================
      else if (sceneName === "anim_cross_session_memory") {
        const r1Pts = [[-6.5, 1.5], [-5.2, -1.2], [-3.8, 1.3], [-2.5, -0.6]];
        r1Pts.forEach(([x, z], idx) =>
          addPedestal(root, x, z, 1.15, 0.92, 1.1, 0xffffff, 0x1e3a8a, "STEP " + (idx + 1), idx === 1 ? "Retry" : "Run 1")
        );
        const r1Path = addTubePath(root, r1Pts.map(([x, z]) => [x, 0.95, z]), 0.06, 0x94a3b8, 0.85);
        const r1Sp = makeCardSprite("RUN 1 (COLD START)", "4 Steps / Fault Hit", "#1E3A8A", "#FFFFFF", 3.2, 2.75);
        r1Sp.position.x = -4.6;
        root.add(r1Sp);

        const dbMesh = new THREE.Mesh(
          new THREE.CylinderGeometry(1.15, 1.15, 2.1, 36),
          new THREE.MeshStandardMaterial({ color: 0x1e3a8a, transparent: true, opacity: 0.24, roughness: 0.15 })
        );
        dbMesh.position.set(0, 1.05, 0);
        root.add(dbMesh);
        const glassWall = new THREE.Mesh(
          new THREE.BoxGeometry(0.08, 3.6, 5.4),
          new THREE.MeshStandardMaterial({ color: 0xe2e8f0, transparent: true, opacity: 0.28, roughness: 0.1 })
        );
        glassWall.position.set(0, 1.8, 0);
        root.add(glassWall);
        root.add(makeCardSprite("CHROMA EPISODIC DB", "Cold Restart Boundary", "#EA580C", "#FFFFFF", 3.3, 3.55));

        addPedestal(root, 2.5, 0.0, 1.4, 1.0, 1.3, 0xffffff, 0x15803d, "RECALL", "AAR Hit");
        addPedestal(root, 6.2, 0.0, 1.4, 1.0, 1.3, 0xffffff, 0x15803d, "SOLVED", "2 Steps");
        const r2Path = addTubePath(root, [[2.5, 1.0, 0.0], [6.2, 1.0, 0.0]], 0.075, 0x15803d, 0.9);
        const r2Sp = makeCardSprite("RUN 2 (WARM RECALL)", "2 Steps (50% Faster)", "#15803D", "#F0FDF4", 3.3, 2.75);
        r2Sp.position.x = 4.4;
        root.add(r2Sp);

        const crystal = addLabeledCube(root, 0.62, 0xea580c, 0xffffff, "AAR", "Rule");
        const pkt = addLabeledCube(root, 0.50, 0x3b82f6, 0xffffff, "EXEC", "Run");

        const commitArc = new THREE.CatmullRomCurve3([
          new THREE.Vector3(-2.5, 1.3, -0.6), new THREE.Vector3(-1.2, 2.5, -0.3), new THREE.Vector3(0, 1.3, 0)
        ]);
        const recallArc = new THREE.CatmullRomCurve3([
          new THREE.Vector3(0, 1.3, 0), new THREE.Vector3(1.2, 2.5, 0), new THREE.Vector3(2.5, 1.3, 0)
        ]);

        activeUpdate = (t) => {
          const p = clamp01(t / totalDuration);
          crystal.rotation.y = t * 1.5;
          pkt.rotation.y = t * 1.2;

          if (p < 0.36) {
            pkt.visible = true;
            pkt.position.copy(r1Path.getPoint(smoothstep(0.04, 0.35, p)));
            pkt.position.y += 0.35;
            crystal.visible = false;
          } else if (p < 0.56) {
            pkt.visible = false;
            crystal.visible = true;
            crystal.position.copy(commitArc.getPoint(smoothstep(0.36, 0.54, p)));
          } else if (p < 0.72) {
            crystal.visible = true;
            crystal.position.copy(recallArc.getPoint(smoothstep(0.56, 0.70, p)));
            pkt.visible = false;
          } else {
            crystal.visible = false;
            pkt.visible = true;
            pkt.position.copy(r2Path.getPoint(smoothstep(0.72, 0.94, p)));
            pkt.position.y += 0.35;
          }

          if (p < 0.35) {
            const u = smoothstep(0, 0.18, p);
            pos.set(lerp(-2.5, -4.6, u), lerp(8.5, 5.5, u), lerp(14.5, 9.0, u));
            look.set(-4.5, 1.2, 0);
            setHud("1 / 4  RUN 1 DISCOVERING SOLUTION IN 4 STEPS", p, "#1E3A8A");
          } else if (p < 0.60) {
            const u = smoothstep(0.35, 0.58, p);
            pos.set(lerp(-4.6, 0.4, u), 5.2, lerp(9.0, 8.0, u));
            look.set(lerp(-4.5, 0.0, u), 1.5, 0);
            setHud("2 / 4  STORING AAR LESSON ACROSS COLD RESTART", p, "#EA580C");
          } else if (p < 0.84) {
            const u = smoothstep(0.60, 0.75, p);
            pos.set(lerp(0.4, 4.4, u), 5.2, lerp(8.0, 8.8, u));
            look.set(lerp(0.0, 4.4, u), 1.2, 0);
            setHud("3 / 4  RUN 2 RECALLING PRECEDENT -> 2 STEPS", p, "#15803D");
          } else {
            const u = smoothstep(0.84, 1.0, p);
            pos.set(lerp(4.4, 0.0, u), lerp(5.2, 8.6, u), lerp(8.8, 15.2, u));
            look.set(lerp(4.4, 0.0, u), 1.4, 0);
            setHud("4 / 4  CROSS-SESSION SPEEDUP VERIFIED (-50%)", p, "#15803D");
          }
          camera.position.copy(pos);
          camera.lookAt(look);
        };
      }

      // =========================================================================
      // SCENE 6: anim_fault_recovery (Labeled Batch B, Sandbox, Quarantine, OK/NaN)
      // =========================================================================
      else if (sceneName === "anim_fault_recovery") {
        addPedestal(root, -3.5, 0, 5.8, 0.38, 1.9, 0xf8fafc, 0xcbd5e1, "BATCH B", "Stream");
        addPedestal(root, 0.4, 0, 1.9, 1.15, 1.9, 0xffffff, 0x1e3a8a, "SANDBOX", "Agent");
        addPedestal(root, 0.2, 2.75, 1.85, 0.35, 1.5, 0xfef2f2, 0xb91c1c, "ISOLATED", "Quarantine");

        const shield = new THREE.Mesh(
          new THREE.CylinderGeometry(1.5, 1.5, 2.0, 32, 1, true),
          new THREE.MeshStandardMaterial({ color: PAL.orange, transparent: true, opacity: 0.22, side: THREE.DoubleSide })
        );
        shield.position.set(0.4, 1.1, 0);
        root.add(shield);
        const sBadge = makeCardSprite("TRY / EXCEPT SHIELD", "Fault Isolation", "#EA580C", "#FFFFFF", 3.2, 3.05);
        sBadge.position.x = 0.4;
        root.add(sBadge);

        const db = new THREE.Mesh(
          new THREE.CylinderGeometry(0.9, 0.9, 1.8, 32),
          new THREE.MeshStandardMaterial({ color: PAL.blue, transparent: true, opacity: 0.28 })
        );
        db.position.set(0.4, 0.9, -3.2);
        root.add(db);
        const pBadge = makeCardSprite("PRECEDENT DB", "Recall Rule", "#1E3A8A", "#FFFFFF", 2.7, 2.4);
        pBadge.position.set(0.4, 2.4, -3.2);
        root.add(pBadge);

        const report = makeScreenBoard(3.8, 2.2, (ctx, w, h, healed) => {
          ctx.fillStyle = "#FFFFFF";
          ctx.fillRect(0, 0, w, h);
          ctx.strokeStyle = healed ? "#15803D" : "#CBD5E1";
          ctx.lineWidth = 8;
          ctx.strokeRect(4, 4, w - 8, h - 8);
          ctx.fillStyle = "#0F172A";
          ctx.font = "700 28px 'Segoe UI', sans-serif";
          ctx.fillText("AUDIT_REPORT.MD", 30, 52);
          ctx.fillStyle = healed ? "#15803D" : "#64748B";
          ctx.font = "700 31px Consolas, monospace";
          ctx.fillText(healed ? "STATUS: PASSED (0 CRASHES)" : "STATUS: SCANNING BATCH B...", 30, 130);
          ctx.fillStyle = "#334155";
          ctx.font = "600 24px Consolas, monospace";
          ctx.fillText(healed ? "Quarantined: NaN_Row_14" : "Records Ingested: ...", 30, 195);
          ctx.fillText(healed ? "Recalled: Chroma_AAR_Rule" : "Shield Armed: try/except", 30, 240);
        });
        report.position.set(4.9, 1.75, 0);
        report.rotation.y = -0.32;
        root.add(report);

        const okBlock = addLabeledCube(root, 0.62, 0x15803d, 0xffffff, "OK", "Valid");
        const badBlock = addLabeledCube(root, 0.68, 0xb91c1c, 0xffffff, "NaN", "Fault");

        activeUpdate = (t) => {
          const p = clamp01(t / totalDuration);
          report.userData.update(p > 0.72);

          if (p < 0.34) {
            badBlock.position.set(lerp(-6.0, -0.8, smoothstep(0.05, 0.34, p)), 0.74, 0);
          } else {
            const q = smoothstep(0.34, 0.58, p);
            badBlock.position.set(lerp(-0.8, 0.2, q), 0.74 + Math.sin(q * Math.PI) * 0.75, lerp(0, 2.75, q));
            badBlock.rotation.z = q * 0.4;
          }

          okBlock.visible = p > 0.40;
          okBlock.position.set(lerp(-5.8, 3.2, smoothstep(0.42, 0.85, p)), 0.74, 0);

          shield.rotation.y = t * 1.2;
          shield.material.opacity = (p > 0.32 && p < 0.48) ? 0.45 : 0.20;

          if (p < 0.22) {
            const u = smoothstep(0, 0.22, p);
            pos.set(-0.4, lerp(9.5, 6.4, u), lerp(15.5, 12.0, u));
            look.set(-0.2, 1.3, -0.3);
            setHud("1 / 4  UNSEEN BATCH B TELEMETRY ARRIVING", p, "#1E3A8A");
          } else if (p < 0.55) {
            const u = smoothstep(0.22, 0.34, p);
            pos.set(lerp(-0.4, 0.4, u), 4.8, lerp(12.0, 8.2, u));
            look.set(0.2, 1.2, 0.5);
            const shake = Math.exp(-Math.pow((p - 0.35) * 20, 2)) * 0.20;
            pos.x += Math.sin(t * 58) * shake;
            setHud(p > 0.34 ? "2 / 4  NAN FAULT QUARANTINED BY SHIELD" : "2 / 4  DETECTING CORRUPT JSON RECORD", p, "#B91C1C");
          } else if (p < 0.76) {
            const u = smoothstep(0.55, 0.68, p);
            pos.set(lerp(0.4, 2.8, u), 4.9, lerp(8.2, 8.2, u));
            look.set(lerp(0.2, 1.3, u), 1.3, -1.4);
            setHud("3 / 4  QUERYING CHROMA PRECEDENT & PROCESSING", p, "#EA580C");
          } else {
            const u = smoothstep(0.76, 1.0, p);
            pos.set(lerp(2.8, 5.2, u), lerp(4.9, 4.3, u), lerp(8.2, 7.6, u));
            look.set(lerp(1.3, 4.6, u), 1.5, 0);
            setHud("4 / 4  CLEAN AUDIT REPORT GENERATED (0 TRACEBACKS)", p, "#15803D");
          }
          camera.position.copy(pos);
          camera.lookAt(look);
        };
      }

      // =========================================================================
      // SCENE 7: anim_rag_pipeline (Docs -> Keyword Fail -> Vector -> Prompt -> LLM -> Answer)
      // =========================================================================
      else if (sceneName === "anim_rag_pipeline") {
        // Left cluster: 3 indexed ECE document pedestals
        const docs = [
          { z: -2.0, lbl: "DOC 1", sub: "irf540n_mosfet.md", col: 0x1e3a8a },
          { z:  0.0, lbl: "DOC 2", sub: "esp32_s3.md",       col: 0x475569 },
          { z:  2.0, lbl: "DOC 3", sub: "5g_nr_prb.md",      col: 0x475569 },
        ];
        docs.forEach((d) => {
          addPedestal(root, -5.6, d.z, 1.85, 0.55, 1.35, 0xffffff, d.col, d.lbl, d.sub);
        });
        const kbBadge = makeCardSprite("KNOWLEDGE BASE", "Local ECE Docs", "#1E3A8A", "#FFFFFF", 2.9, 2.35);
        kbBadge.position.set(-5.6, 2.35, -2.2);
        root.add(kbBadge);

        // Gates at center-left (x = -2.2): Red Keyword gate & Green Cosine Vector gate
        const kwGate = new THREE.Mesh(
          new THREE.BoxGeometry(0.28, 2.3, 4.4),
          new THREE.MeshStandardMaterial({ color: PAL.red, transparent: true, opacity: 0.24, roughness: 0.2 })
        );
        kwGate.position.set(-2.2, 1.15, 0);
        const kwEdges = new THREE.LineSegments(
          new THREE.EdgesGeometry(new THREE.BoxGeometry(0.28, 2.3, 4.4)),
          new THREE.LineBasicMaterial({ color: PAL.red })
        );
        kwGate.add(kwEdges);
        root.add(kwGate);
        const kwBadge = makeCardSprite("CTRL+F KEYWORD", "0 Exact Hits", "#B91C1C", "#FEF2F2", 2.75, 2.95);
        kwBadge.position.set(-2.2, 2.95, 0);
        root.add(kwBadge);

        const vecGate = new THREE.Mesh(
          new THREE.BoxGeometry(0.28, 2.3, 4.4),
          new THREE.MeshStandardMaterial({ color: PAL.green, transparent: true, opacity: 0.22, roughness: 0.2 })
        );
        vecGate.position.set(-2.2, 1.15, 0);
        const vecEdges = new THREE.LineSegments(
          new THREE.EdgesGeometry(new THREE.BoxGeometry(0.28, 2.3, 4.4)),
          new THREE.LineBasicMaterial({ color: PAL.green })
        );
        vecGate.add(vecEdges);
        vecGate.visible = false;
        root.add(vecGate);
        const vecBadge = makeCardSprite("COSINE VECTOR", "2 Chunks Found", "#15803D", "#F0FDF4", 2.85, 2.95);
        vecBadge.position.set(-2.2, 2.95, 0);
        vecBadge.visible = false;
        root.add(vecBadge);

        // Center-right: Dark Prompt Box + Blue LLM Cube + Green Answer Panel
        const promptPed = addPedestal(root, 1.4, 0.0, 2.3, 1.15, 2.0, 0x0b1220, 0xea580c, "PROMPT", "Context + Q", "#EA580C");
        const promptBadge = makeCardSprite("SYSTEM PROMPT", "Grounded Context", "#EA580C", "#FFFFFF", 2.75, 2.45);
        promptBadge.position.set(1.4, 2.45, 0);
        root.add(promptBadge);

        const llmCube = addLabeledCube(root, 1.35, PAL.blue, 0xffffff, "LLM", "Groq 8B");
        llmCube.position.set(4.5, 1.15, 0);
        addPedestal(root, 4.5, 0.0, 1.9, 0.35, 1.9, 0xf8fafc, 0x1e3a8a);
        const llmBadge = makeCardSprite("LLM INFERENCE", "Reads Context Only", "#1E3A8A", "#FFFFFF", 2.65, 2.55);
        llmBadge.position.set(4.5, 2.55, 0);
        root.add(llmBadge);

        const ansBoard = makeScreenBoard(3.3, 1.95, (ctx, w, h, ready) => {
          ctx.fillStyle = "#FFFFFF";
          ctx.fillRect(0, 0, w, h);
          ctx.strokeStyle = ready ? "#15803D" : "#CBD5E1";
          ctx.lineWidth = 8;
          ctx.strokeRect(4, 4, w - 8, h - 8);
          ctx.fillStyle = "#64748B";
          ctx.font = "700 22px Consolas, monospace";
          ctx.fillText("GROUNDED ANSWER", 28, 48);
          ctx.fillStyle = ready ? "#15803D" : "#94A3B8";
          ctx.font = "700 38px 'Segoe UI', sans-serif";
          ctx.fillText(ready ? "Max Vds = 100 V" : "Waiting...", 28, 130);
          ctx.fillStyle = ready ? "#0F172A" : "#94A3B8";
          ctx.font = "700 24px Consolas, monospace";
          ctx.fillText(ready ? "[irf540n_mosfet.md]" : "No context yet", 28, 200);
          ctx.fillText(ready ? "dist = 0.72 (Top-1)" : "", 28, 245);
        });
        ansBoard.position.set(7.8, 1.65, 0);
        ansBoard.rotation.y = -0.32;
        root.add(ansBoard);

        // Beam from Prompt -> LLM
        const beamCurve = addTubePath(root, [[2.55, 1.0, 0], [3.8, 1.15, 0]], 0.055, PAL.orange, 0.85);

        // Moving Query Sphere & Extracted Chunk Cubes
        const querySphere = new THREE.Mesh(
          new THREE.SphereGeometry(0.38, 28, 28),
          new THREE.MeshStandardMaterial({ color: PAL.blueLt, roughness: 0.2, metalness: 0.1 })
        );
        querySphere.castShadow = true;
        root.add(querySphere);
        const qTag = makeCardSprite("QUERY", "max Vds?", "#1E3A8A", "#EFF6FF", 1.85, 1.1);
        querySphere.add(qTag);

        const chunkA = addLabeledCube(root, 0.52, PAL.orange, 0xffffff, "CHUNK 3", "d=0.72");
        const chunkB = addLabeledCube(root, 0.52, PAL.orange, 0xffffff, "CHUNK 7", "d=0.89");

        const arcA = new THREE.CatmullRomCurve3([
          new THREE.Vector3(-5.6, 0.85, -2.0), new THREE.Vector3(-2.0, 2.3, -1.2), new THREE.Vector3(1.4, 1.35, -0.3)
        ]);
        const arcB = new THREE.CatmullRomCurve3([
          new THREE.Vector3(-5.6, 0.85, -2.0), new THREE.Vector3(-2.0, 1.85, 0.6), new THREE.Vector3(1.4, 1.35, 0.3)
        ]);

        activeUpdate = (t) => {
          const p = clamp01(t / totalDuration);
          ansBoard.userData.update(p >= 0.80);

          // Query sphere movement (0.13 -> 0.40)
          if (p < 0.27) {
            querySphere.visible = true;
            querySphere.position.set(lerp(-8.2, -2.75, smoothstep(0.12, 0.27, p)), 1.0, 0);
          } else if (p < 0.42) {
            // Rebound slightly at red gate then wait
            const bounce = Math.sin(smoothstep(0.27, 0.36, p) * Math.PI) * 0.45;
            querySphere.position.set(-2.75 - bounce, 1.0, 0);
          } else if (p < 0.62) {
            querySphere.position.set(lerp(-2.75, 0.1, smoothstep(0.42, 0.58, p)), 1.0, 0);
          } else {
            querySphere.visible = false;
          }

          // Gates swap at p = 0.40
          const vectorActive = p >= 0.40;
          kwGate.visible = !vectorActive;
          kwBadge.visible = p >= 0.27 && !vectorActive;
          vecGate.visible = vectorActive;
          vecBadge.visible = vectorActive;

          // Orange chunk cubes extract (0.42 -> 0.67)
          chunkA.visible = p >= 0.42 && p < 0.72;
          chunkB.visible = p >= 0.46 && p < 0.72;
          if (chunkA.visible) {
            chunkA.position.copy(arcA.getPoint(smoothstep(0.42, 0.66, p)));
            chunkA.rotation.y = t * 1.6;
          }
          if (chunkB.visible) {
            chunkB.position.copy(arcB.getPoint(smoothstep(0.46, 0.68, p)));
            chunkB.rotation.y = -t * 1.4;
          }

          // LLM cube spin
          const llmSpin = (p >= 0.66 && p <= 0.82) ? 3.2 : 0.7;
          llmCube.rotation.y = t * llmSpin;
          promptPed.position.y = (p >= 0.60 && p <= 0.70) ? 0.66 : 0.575;

          // Answer panel slide-in
          ansBoard.visible = p >= 0.78;
          ansBoard.position.x = lerp(6.8, 7.8, smoothstep(0.78, 0.88, p));

          // Camera & HUD choreography matching storyboard
          if (p < 0.13) {
            const u = smoothstep(0.0, 0.13, p);
            pos.set(lerp(-7.5, -6.2, u), lerp(6.2, 5.2, u), lerp(10.5, 9.2, u));
            look.set(-5.0, 1.0, 0);
            setHud("1 / 7  KNOWLEDGE BASE: 3 ECE DATASHEETS", p, "#1E3A8A");
          } else if (p < 0.27) {
            const u = smoothstep(0.13, 0.27, p);
            pos.set(lerp(-6.2, -3.5, u), 5.0, lerp(9.2, 8.8, u));
            look.set(lerp(-5.0, -2.5, u), 1.1, 0);
            setHud("2 / 7  USER QUESTION: 'MAX VDS?'", p, "#1E3A8A");
          } else if (p < 0.40) {
            const shake = Math.exp(-Math.pow((p - 0.30) * 22, 2)) * 0.20;
            pos.set(-3.2 + Math.sin(t * 55) * shake, 4.9 + Math.cos(t * 48) * shake, 8.6);
            look.set(-2.3, 1.2, 0);
            setHud("3 / 7  KEYWORD SEARCH: 0 EXACT MATCHES", p, "#B91C1C");
          } else if (p < 0.57) {
            const u = smoothstep(0.40, 0.57, p);
            pos.set(lerp(-3.2, -0.8, u), 5.1, lerp(8.6, 9.4, u));
            look.set(lerp(-2.3, -0.5, u), 1.2, 0);
            setHud("4 / 7  VECTOR SEARCH: 2 CLOSEST CHUNKS", p, "#15803D");
          } else if (p < 0.67) {
            const u = smoothstep(0.57, 0.67, p);
            pos.set(lerp(-0.8, 1.6, u), 4.9, lerp(9.4, 8.6, u));
            look.set(lerp(-0.5, 1.4, u), 1.2, 0);
            setHud("5 / 7  CONTEXT LOADED INTO PROMPT BOX", p, "#EA580C");
          } else if (p < 0.80) {
            const u = smoothstep(0.67, 0.80, p);
            pos.set(lerp(1.6, 4.6, u), 4.8, lerp(8.6, 8.4, u));
            look.set(lerp(1.4, 4.6, u), 1.3, 0);
            setHud("6 / 7  LLM READING RETRIEVED CONTEXT", p, "#1E3A8A");
          } else {
            const u = smoothstep(0.80, 0.94, p);
            pos.set(lerp(4.6, 1.1, u), lerp(4.8, 8.4, u), lerp(8.4, 15.8, u));
            look.set(lerp(4.6, 1.0, u), 1.2, 0);
            setHud("7 / 7  GROUNDED ANSWER: 100 V [IRF540N_MOSFET.MD]", p, "#15803D");
          }
          camera.position.copy(pos);
          camera.lookAt(look);
        };
      }

      window.renderFrame = function(t) {
        activeUpdate(t);
        renderer.render(scene, camera);
      };
      window.renderFrame(0);
    };
  </script>
</body>
</html>`;

async function startStaticServer() {
  const threeModule = fs.readFileSync(path.join(THREE_DIR, "three.module.js"));
  const threeCore = fs.readFileSync(path.join(THREE_DIR, "three.core.js"));
  const server = http.createServer((req, res) => {
    if (req.url === "/three.module.js") {
      res.writeHead(200, { "Content-Type": "application/javascript" });
      return res.end(threeModule);
    }
    if (req.url === "/three.core.js") {
      res.writeHead(200, { "Content-Type": "application/javascript" });
      return res.end(threeCore);
    }
    res.writeHead(200, { "Content-Type": "text/html; charset=utf-8" });
    return res.end(HTML_TEMPLATE);
  });
  await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
  const addr = server.address();
  return { server, url: `http://127.0.0.1:${addr.port}/` };
}

async function renderSceneVideo(page, url, spec) {
  const mp4Path = path.join(VIDEOS_DIR, `${spec.name}.mp4`);
  const posterPath = path.join(VIDEOS_DIR, `${spec.name}_poster.png`);

  await page.goto(url, { waitUntil: "domcontentloaded" });
  await page.evaluate((name, sub, dur) => {
    window.initScene(name, sub, dur);
  }, spec.name, spec.subtitle, spec.duration);

  const ff = spawn("ffmpeg", [
    "-y",
    "-f", "image2pipe",
    "-vcodec", "mjpeg",
    "-framerate", String(FPS),
    "-i", "-",
    "-vf", "format=yuv420p",
    "-color_range", "tv",
    "-c:v", "libx264",
    "-profile:v", "main",
    "-level", "4.1",
    "-pix_fmt", "yuv420p",
    "-preset", "medium",
    "-crf", "20",
    "-movflags", "+faststart",
    mp4Path,
  ], { stdio: ["pipe", "ignore", "pipe"] });

  let errText = "";
  ff.stderr.on("data", (d) => { errText += d.toString(); });

  const totalFrames = Math.ceil(spec.duration * FPS);
  const posterIdx = Math.round(spec.posterT * FPS);

  for (let i = 0; i < totalFrames; i++) {
    const t = i / FPS;
    await page.evaluate((timeSec) => { window.renderFrame(timeSec); }, t);
    const jpgBuf = await page.screenshot({ type: "jpeg", quality: 92 });
    if (!ff.stdin.write(jpgBuf)) {
      await new Promise((r) => ff.stdin.once("drain", r));
    }
    if (i === posterIdx) {
      await page.screenshot({ path: posterPath, type: "png" });
    }
  }
  ff.stdin.end();
  const exitCode = await new Promise((resolve) => ff.on("close", resolve));
  if (exitCode !== 0) {
    throw new Error(`ffmpeg failed for ${spec.name} (code ${exitCode}): ${errText.slice(-500)}`);
  }
  console.log(`Rendered ${spec.name}.mp4 (${totalFrames} frames, ${spec.duration}s) + poster`);
}

async function main() {
  const { server, url } = await startStaticServer();
  const browser = await puppeteer.launch({
    executablePath: CHROME_PATH,
    headless: true,
    protocolTimeout: 0,
    args: [
      "--no-sandbox",
      "--disable-setuid-sandbox",
      "--disable-dev-shm-usage",
      "--enable-webgl",
      "--ignore-gpu-blocklist",
      `--window-size=${W},${H}`,
    ],
    defaultViewport: { width: W, height: H, deviceScaleFactor: 1 },
  });

  try {
    const page = await browser.newPage();
    page.on("pageerror", (e) => console.error("[PAGEERROR]", e.message));
    const filter = process.argv[2] || "";
    for (const spec of SCENES) {
      if (filter && !spec.name.includes(filter)) continue;
      await renderSceneVideo(page, url, spec);
    }
  } finally {
    await browser.close();
    server.close();
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
