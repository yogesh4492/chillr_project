// Chillr — main script

// Post menu toggle
document.querySelectorAll('.post-more-btn').forEach(btn => {
  btn.addEventListener('click', e => {
    e.stopPropagation();
    const menu = btn.closest('.post-menu');
    document.querySelectorAll('.post-menu.open').forEach(m => { if(m !== menu) m.classList.remove('open'); });
    menu.classList.toggle('open');
  });
});
document.addEventListener('click', () => {
  document.querySelectorAll('.post-menu.open').forEach(m => m.classList.remove('open'));
});

// Like toggle
document.querySelectorAll('.like-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    btn.classList.toggle('liked');
    const icon = btn.querySelector('.material-icons');
    icon.textContent = btn.classList.contains('liked') ? 'favorite' : 'favorite_border';
  });
});

// Bookmark toggle
document.querySelectorAll('.bookmark-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const icon = btn.querySelector('.material-icons');
    icon.textContent = icon.textContent.trim() === 'bookmark_border' ? 'bookmark' : 'bookmark_border';
  });
});

// Follow buttons
document.querySelectorAll('.follow-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const isFollowing = btn.dataset.following === 'true';
    btn.dataset.following = isFollowing ? 'false' : 'true';
    btn.textContent = isFollowing ? 'Follow' : 'Following';
    btn.style.color = isFollowing ? 'var(--accent)' : 'var(--text-3)';
  });
});
