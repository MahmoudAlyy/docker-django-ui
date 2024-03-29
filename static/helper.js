function updatePage(ajaxURL) {
   document.getElementById('refresh').innerHTML = "Loading...";

   let url = window.location.href + ajaxURL;
   fetch(url, {
      method: "GET",
   }).then((response) => {
      return response.text()
   }).then((html) => {
      document.getElementById('refresh').innerHTML = "Refresh";
      document.getElementById('content').innerHTML = html;
   })
}


function uniqueID() {
   return Math.floor(Math.random() * Date.now())
}


function createToastAlert(msg, isFailure) {

   let div_id = uniqueID();

   const toastHtml =
      `<div id="` + div_id + `" class="toast align-items-center text-white bg-primary border-0" role="alert" aria-live="assertive" aria-atomic="true">
       <div class="d-flex">
          <div class="toast-body">`
      + msg +
      `</div>
          <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"
             aria-label="Close"></button>
       </div>
    </div>
    `;

   var toastContainer = document.getElementById('toastContainer');
   toastContainer.innerHTML += toastHtml;

   // if failure msg, make background color red
   if (isFailure) {
      $('#' + div_id).removeClass('bg-primary').addClass('bg-danger');
   }

   $('#' + div_id).toast('show')
   setTimeout(function () {
      $('#' + div_id).toast('hide')

   }, 5000);
}


function sleep(ms) {
   return new Promise(resolve => setTimeout(resolve, ms));
}


async function getUpdate(task_id) {
   var flag = true;
   let progressUrl = window.location.href + '../get_progress/';

   while (flag) {

      await sleep(2000);
      await fetch(progressUrl + task_id)
         .then(response => response.json())
         .then(data => {
            console.log(data)
            console.log(data['state'])

            if (data['state'] == 'SUCCESS') {
               flag = false;
               let msg = data['details']
               createToastAlert(msg, false)
            }

            else if (data['state'] == 'FAILURE') {
               flag = false;
               let msg = data['details']
               createToastAlert(msg, true)

            }
         })
   }
   return
}


