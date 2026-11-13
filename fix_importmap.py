# -*- coding: utf-8 -*-
import re

html_path = r'C:\Users\goodt\island-avatar-scene\index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Clean importmap: remove any JS code inside <script type="importmap">...</script>
clean_importmap = '''<script type="importmap">
    {
      "imports": {
        "three": "https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js",
        "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"
      }
    }
  </script>'''

text = re.sub(r'<script type="importmap">.*?</script>', clean_importmap, text, flags=re.DOTALL)

# 2. Check and inject album JS to the end of the module script
story_album_funcs = '''
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
    if (typeof initAudio === 'function') initAudio();
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

last_script_end = text.rfind('</script>')
if last_script_end != -1:
    # Remove existing album functions if duplicate
    text = text.replace(story_album_funcs, '')
    last_script_end = text.rfind('</script>')
    text = text[:last_script_end] + '\n' + story_album_funcs + '\n  ' + text[last_script_end:]

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(text)

# Sync to inchan-mind-basket
dst_path = r'C:\Users\goodt\Desktop\2026 사회정서학습 연구회 프로젝트\inchan-mind-basket\index.html'
with open(dst_path, 'w', encoding='utf-8') as f:
    f.write(text)

print('[SUCCESS] Cleaned importmap and fixed script injection!')
