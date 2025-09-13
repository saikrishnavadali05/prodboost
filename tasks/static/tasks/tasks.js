document.addEventListener('DOMContentLoaded', ()=>{
  document.querySelectorAll('.incr').forEach(btn=>{
    btn.addEventListener('click', async (e)=>{
      const wrapper = e.target.closest('.task')
      const id = wrapper.dataset.taskId
      const step = e.target.dataset.step || 1
      const resp = await fetch(`/api/tasks/${id}/progress/`, {
        method: 'POST', headers: {'Content-Type':'application/json'},
        body: JSON.stringify({action:'incr', step})
      })
      const data = await resp.json()
      // update UI
      const bar = wrapper.querySelector('.bar')
      const percent = data.percent || Math.round((data.completed_steps/data.total_steps)*100)
      bar.style.width = percent + '%'
      wrapper.querySelector('small').textContent = `${data.completed_steps} / ${data.total_steps} (${data.status})`
    })
  })

  // detail page buttons
  const incrBtn = document.getElementById('incr-1')
  if (incrBtn){
    incrBtn.addEventListener('click', async ()=>{
      const id = window.location.pathname.split('/').filter(Boolean).slice(-1)[0]
      const resp = await fetch(`/api/tasks/${id}/progress/`, {
        method:'POST', headers:{'Content-Type':'application/json'},
        body: JSON.stringify({action:'incr', step:1})
      })
      const data = await resp.json()
      const bar = document.getElementById('bar-' + id)
      const percent = data.percent || Math.round((data.completed_steps/data.total_steps)*100)
      bar.style.width = percent + '%'
      document.getElementById('meta-' + id).textContent = `${data.completed_steps} / ${data.total_steps} (${data.status})`
    })
  }
})
