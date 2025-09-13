// tasks.js
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + "=")) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
const csrftoken = getCookie("csrftoken");

document.addEventListener('DOMContentLoaded', ()=>{
  // list page (+1 buttons)
  document.querySelectorAll('.incr').forEach(btn=>{
    btn.addEventListener('click', async (e)=>{
      const wrapper = e.target.closest('.task');
      const id = wrapper.dataset.taskId;
      const step = e.target.dataset.step || 1;

      const resp = await fetch(`/api/tasks/${id}/progress/`, {
        method: 'POST',
        headers: {
          'Content-Type':'application/json',
          'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({action:'incr', step})
      });

      const data = await resp.json();
      updateTaskUI(wrapper, data);
    });
  });

  // detail page buttons
  const incrBtn = document.getElementById('incr-1');
  if (incrBtn){
    incrBtn.addEventListener('click', async ()=>{
      const id = window.location.pathname.split('/').filter(Boolean).slice(-1)[0];
      const resp = await fetch(`/api/tasks/${id}/progress/`, {
        method:'POST',
        headers:{
          'Content-Type':'application/json',
          'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({action:'incr', step:1})
      });
      const data = await resp.json();
      updateTaskUIDetail(id, data);
    });
  }

  // detail page reset button
  const resetBtn = document.getElementById('reset-0');
  if (resetBtn){
    resetBtn.addEventListener('click', async ()=>{
      const id = window.location.pathname.split('/').filter(Boolean).slice(-1)[0];
      const resp = await fetch(`/api/tasks/${id}/progress/`, {
        method:'POST',
        headers:{
          'Content-Type':'application/json',
          'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({action:'reset'})
      });
      const data = await resp.json();
      updateTaskUIDetail(id, data);
    });
  }
});

function updateTaskUI(wrapper, data){
  const bar = wrapper.querySelector('.bar');
  const percent = data.percent || Math.round((data.completed_steps/data.total_steps)*100);
  bar.style.width = percent + '%';
  wrapper.querySelector('small').textContent =
    `${data.completed_steps} / ${data.total_steps} (${data.status})`;
}

function updateTaskUIDetail(id, data){
  const bar = document.getElementById('bar-' + id);
  const percent = data.percent || Math.round((data.completed_steps/data.total_steps)*100);
  bar.style.width = percent + '%';
  document.getElementById('meta-' + id).textContent =
    `${data.completed_steps} / ${data.total_steps} (${data.status})`;
}
