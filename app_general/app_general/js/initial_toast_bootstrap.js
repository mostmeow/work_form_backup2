
const toastTrigger = document.getElementById('liveToastBtn')
const toastLive = document.getElementById('successToast')

// if (toastTrigger) {
//     toastTrigger.addEventListener('click', () => {
//         const toast = new bootstrap.Toast(toastLiveExample)

//         toast.show()
//     })
// }

window.onload = () => {
    const toast = new bootstrap.Toast(toastLive)

    toast.show()
}