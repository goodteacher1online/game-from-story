# -*- coding: utf-8 -*-
import os

html_path = r'C:\Users\goodt\island-avatar-scene\index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Add Stardust & Story Album Button to HUD
target_hud = '''<span class="quest-count" id="questCountText">0/5</span>
        </div>'''

replacement_hud = '''<span class="quest-count" id="questCountText">0/5</span>
          <div style="display:inline-flex; align-items:center; gap:4px; margin-left:10px; font-weight:700; color:#fbbf24;" title="마음 별가루 수집">
            <span style="font-size:14px;">★</span><span id="stardustText">0/15</span>
          </div>
        </div>
        <button class="hw-btn" onclick="openStoryBookModal()" style="border-color:rgba(251,191,36,0.4); color:#fbbf24; font-weight:700;">
          <span style="font-size:14px;">📖</span> 동화책 앨범
        </button>'''

if target_hud in text:
    text = text.replace(target_hud, replacement_hud)
    print('[OK] HUD updated with Stardust and Story Album button')

# 2. Add Story Album Modal and Mom Dialog to HTML
modal_html = '''
  <!-- =========================================
       원작 《인찬이의 마음 손님》 33컷 동화책 앨범 모달
       ========================================= -->
  <div id="storyBookModal" style="display:none; position:fixed; inset:0; z-index:9999; background:rgba(15,23,42,0.88); backdrop-filter:blur(16px); align-items:center; justify-content:center;">
    <div style="background:#1e293b; border:1px solid rgba(255,255,255,0.15); border-radius:20px; width:90%; max-width:680px; max-height:85vh; padding:24px; box-shadow:0 25px 50px -12px rgba(0,0,0,0.7); display:flex; flex-direction:column; color:#f8fafc;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
        <div style="display:flex; align-items:center; gap:8px;">
          <span style="background:#fbbf24; color:#0f172a; font-weight:800; font-size:12px; padding:3px 8px; border-radius:6px;">원작 동화 컬렉션</span>
          <h3 id="albumTitle" style="font-size:18px; font-weight:700; color:#fff;">인찬이의 마음 손님 (33컷)</h3>
        </div>
        <button onclick="closeStoryBookModal()" style="background:rgba(255,255,255,0.1); border:none; color:#cbd5e1; font-size:16px; width:32px; height:32px; border-radius:50%; cursor:pointer;">✕</button>
      </div>

      <div style="flex:1; overflow-y:auto; text-align:center; padding:4px;">
        <img id="albumImage" src="assets/inchan/부엌_3D입체공간_마스터시트.jpg" style="max-width:100%; max-height:48vh; border-radius:12px; object-fit:contain; background:#000; box-shadow:0 8px 24px rgba(0,0,0,0.5);" />
        <p id="albumCaption" style="margin-top:14px; font-size:14.5px; line-height:1.6; color:#e2e8f0; font-weight:500;">인찬이의 마음 광주리 세계에 오신 것을 환영합니다.</p>
      </div>

      <div style="display:flex; justify-content:space-between; align-items:center; margin-top:16px; border-top:1px solid rgba(255,255,255,0.1); padding-top:14px;">
        <button onclick="prevAlbumScene()" class="hw-btn" style="background:#334155; color:#fff;">◀ 이전 장면</button>
        <span id="albumPageText" style="font-size:13px; font-weight:700; color:#fbbf24;">1 / 33</span>
        <button onclick="nextAlbumScene()" class="hw-btn" style="background:#334155; color:#fff;">다음 장면 ▶</button>
      </div>
    </div>
  </div>

  <!-- 엄마 NPC 대화 다이얼로그 -->
  <div id="momDialog" style="display:none; position:fixed; bottom:90px; left:50%; transform:translateX(-50%); z-index:9000; background:rgba(30,41,59,0.95); backdrop-filter:blur(16px); border:1.5px solid #fbbf24; border-radius:18px; padding:18px 24px; max-width:520px; width:90%; box-shadow:0 20px 40px rgba(0,0,0,0.6); color:#fff;">
    <div style="display:flex; align-items:center; gap:8px; margin-bottom:8px;">
      <span style="background:#fbbf24; color:#0f172a; font-weight:800; font-size:11px; padding:3px 8px; border-radius:6px;">엄마의 따뜻한 말</span>
      <h4 style="font-size:16px; font-weight:700;">온화한 미소의 엄마</h4>
    </div>
    <p id="momDialogText" style="font-size:14.5px; line-height:1.6; color:#f1f5f9; margin-bottom:12px;">"인찬아, 무슨 일 있어? 사실 사람에게는 누구나 이상한 광주리가 있단다. 마음 광주리라고 하지. 어떤 감정 손님이 찾아오든 엄마가 항상 네 편이란다."</p>
    <div style="display:flex; justify-content:flex-end;">
      <button onclick="document.getElementById('momDialog').style.display='none'" class="hw-btn" style="background:#fbbf24; color:#0f172a; font-weight:800;">알겠어요, 엄마!</button>
    </div>
  </div>
'''

if 'id="storyBookModal"' not in text:
    text = text.replace('</body>', modal_html + '\n</body>')
    print('[OK] Modal HTML injected')

# 3. Add Bounce Pads and Stardust JS definition before animate loop
game_logic_code = '''
    // ==========================================
    // [게이미피케이션 강화] 슈퍼 점프 패드 & 황금 별가루 수집 루프
    // ==========================================
    const bouncePads = [];
    const bouncePadPositions = [
      { x: -14, y: 0.1, z: 12, label: '서쪽 구름 점프대' },
      { x: 18, y: 0.1, z: -10, label: '동쪽 섬 활공 점프대' },
      { x: -25, y: 4.1, z: -40, label: '하늘섬 도약 스프링' },
      { x: 12, y: 0.1, z: 28, label: '남쪽 정원 트램펄린' }
    ];

    bouncePadPositions.forEach((bp, idx) => {
      const padGroup = new THREE.Group();
      padGroup.position.set(bp.x, bp.y, bp.z);
      
      const baseMesh = new THREE.Mesh(
        new THREE.CylinderGeometry(1.4, 1.6, 0.2, 24),
        new THREE.MeshStandardMaterial({ color: 0x3b82f6, roughness: 0.4, metalness: 0.3 })
      );
      padGroup.add(baseMesh);

      const springCore = new THREE.Mesh(
        new THREE.CylinderGeometry(1.0, 1.2, 0.28, 24),
        new THREE.MeshStandardMaterial({
          color: 0x60a5fa, emissive: 0x3b82f6, emissiveIntensity: 0.7, roughness: 0.2
        })
      );
      springCore.position.y = 0.12;
      padGroup.add(springCore);

      const ringEmblem = new THREE.Mesh(
        new THREE.RingGeometry(0.5, 0.75, 24),
        new THREE.MeshBasicMaterial({ color: 0xfde047, side: THREE.DoubleSide })
      );
      ringEmblem.rotation.x = -Math.PI / 2;
      ringEmblem.position.y = 0.27;
      padGroup.add(ringEmblem);

      worldGroup.add(padGroup);
      bouncePads.push({ group: padGroup, pos: new THREE.Vector3(bp.x, bp.y, bp.z), label: bp.label });
    });

    // 15개 황금 마음 별가루 (Stardust Gems)
    const stardustGems = [];
    let collectedStardust = 0;
    const stardustCoords = [
      [2, 1.2, 4], [-4, 1.2, 6], [8, 1.5, -4], [-8, 2.0, -12],
      [-16, 2.5, 8], [14, 1.8, 14], [-2, 1.5, 22], [4, 1.5, 18],
      [-12, 1.8, -2], [10, 2.2, -18], [-20, 6.0, -35], [-30, 8.0, -50],
      [16, 3.0, 4], [0, 2.5, -10], [-6, 1.8, 16]
    ];

    stardustCoords.forEach((coord, idx) => {
      const starGeo = new THREE.OctahedronGeometry(0.28, 0);
      const starMat = new THREE.MeshStandardMaterial({
        color: 0xfbbf24, emissive: 0xf59e0b, emissiveIntensity: 0.9, roughness: 0.2, metalness: 0.5
      });
      const starMesh = new THREE.Mesh(starGeo, starMat);
      starMesh.position.set(coord[0], coord[1], coord[2]);
      worldGroup.add(starMesh);

      const ring = new THREE.Mesh(
        new THREE.TorusGeometry(0.38, 0.02, 8, 20),
        new THREE.MeshBasicMaterial({ color: 0xfde047, transparent: true, opacity: 0.7 })
      );
      ring.rotation.x = Math.PI / 3;
      starMesh.add(ring);

      stardustGems.push({ mesh: starMesh, collected: false, baseY: coord[1], phase: idx * 0.7 });
    });

    function soundCoin() {
      if (!audioCtx) return;
      playTone(587.33, 880, 0.15, 'triangle');
      setTimeout(() => playTone(880, 1174.66, 0.22, 'triangle'), 60);
    }

    function soundSpring() {
      if (!audioCtx) return;
      playTone(200, 650, 0.35, 'sine');
    }

    function soundMomVoice() {
      if (!audioCtx) return;
      playTone(392, 523.25, 0.25, 'sine');
      setTimeout(() => playTone(523.25, 659.25, 0.35, 'sine'), 100);
    }
'''

if 'bouncePads = [];' not in text:
    text = text.replace('function animate(', game_logic_code + '\n    function animate(')
    print('[OK] Bounce pads & stardust logic injected')

# 4. Inject bounce pad & stardust physics check
target_physics = '''      // 바닥 판정 (단순 평면 y=0, 향후 높이맵 확장 가능)'''
replacement_physics = '''      // [게이미피케이션] 슈퍼 점프 패드 충돌 판정
      bouncePads.forEach(bp => {
        const d = Math.hypot(playerRig.position.x - bp.pos.x, playerRig.position.z - bp.pos.z);
        if (d < 1.6 && Math.abs(playerRig.position.y - bp.pos.y) < 1.2 && playerPhysics.velY <= 0) {
          playerPhysics.velY = 22.0;
          playerPhysics.jumpCount = 1;
          playerPhysics.isGrounded = false;
          soundSpring();
          showToast(`⚡ ${bp.label}! 하늘 높이 솟구칩니다!`);
          bp.group.scale.set(1.2, 0.6, 1.2);
          setTimeout(() => bp.group.scale.set(1, 1, 1), 250);
        }
      });

      // [게이미피케이션] 황금 별가루 수집 루프
      stardustGems.forEach(sg => {
        if (!sg.collected) {
          sg.mesh.rotation.y += 0.04;
          sg.mesh.position.y = sg.baseY + Math.sin(timeSec * 3 + sg.phase) * 0.15;
          const d = playerRig.position.distanceTo(sg.mesh.position);
          if (d < 1.4) {
            sg.collected = true;
            sg.mesh.visible = false;
            collectedStardust++;
            soundCoin();
            const textEl = document.getElementById('stardustText');
            if (textEl) textEl.textContent = `${collectedStardust}/15`;
            showToast(`★ 마음 별가루 획득! (${collectedStardust}/15)`);
          }
        }
      });

      // [엄마 NPC 상호작용 검사]
      const distMom = Math.hypot(playerRig.position.x - 6.5, playerRig.position.z - 6.5);
      if (distMom < 2.8) {
        showInteractionHint('[E] 엄마와 이야기하기');
        if (keys.KeyE) {
          keys.KeyE = false;
          const momDlg = document.getElementById('momDialog');
          if (momDlg) {
            momDlg.style.display = 'block';
            soundMomVoice();
          }
        }
      }

      // 바닥 판정 (단순 평면 y=0, 향후 높이맵 확장 가능)'''

if target_physics in text:
    text = text.replace(target_physics, replacement_physics)
    print('[OK] Physics loop updated')

# 5. Add Story Album JS functions to window
story_album_js = '''
  // ==========================================
  // 동화책 앨범 모달 제어 함수
  // ==========================================
  let albumScenes = [];
  let currentAlbumIdx = 0;

  async function loadAlbumData() {
    try {
      const res = await fetch('assets/inchan/scenes_data.json');
      albumScenes = await res.json();
    } catch(e) {
      console.warn('동화 앨범 데이터 로드 대기', e);
    }
  }
  loadAlbumData();

  window.openStoryBookModal = function() {
    initAudio();
    const modal = document.getElementById('storyBookModal');
    if (modal) {
      modal.style.display = 'flex';
      updateAlbumView();
    }
  };

  window.closeStoryBookModal = function() {
    const modal = document.getElementById('storyBookModal');
    if (modal) modal.style.display = 'none';
  };

  window.prevAlbumScene = function() {
    if (albumScenes.length === 0) return;
    currentAlbumIdx = (currentAlbumIdx - 1 + albumScenes.length) % albumScenes.length;
    updateAlbumView();
  };

  window.nextAlbumScene = function() {
    if (albumScenes.length === 0) return;
    currentAlbumIdx = (currentAlbumIdx + 1) % albumScenes.length;
    updateAlbumView();
  };

  function updateAlbumView() {
    if (albumScenes.length === 0) return;
    const cur = albumScenes[currentAlbumIdx];
    document.getElementById('albumImage').src = cur.path;
    document.getElementById('albumTitle').textContent = `${cur.chapter}: ${cur.title}`;
    document.getElementById('albumCaption').textContent = `《인찬이의 마음 손님》 원작 마스터 일러스트 (${currentAlbumIdx + 1}/33)`;
    document.getElementById('albumPageText').textContent = `${currentAlbumIdx + 1} / ${albumScenes.length}`;
  }
'''

if 'window.openStoryBookModal' not in text:
    text = text.replace('</script>', story_album_js + '\n</script>')
    print('[OK] Story album JS injected')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(text)

# Sync to inchan-mind-basket
dst_path = r'C:\Users\goodt\Desktop\2026 사회정서학습 연구회 프로젝트\inchan-mind-basket\index.html'
with open(dst_path, 'w', encoding='utf-8') as f:
    f.write(text)

print('All upgrades successfully applied to both projects!')
