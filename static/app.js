<py-script src="./x.py"></py-script>

const user_first_name = document.getElementById("user_first_name");
const user_last_name = document.getElementById("user_last_name");
const user_email = document.getElementById("user_email");
const user_password = document.getElementById("user_password");

const button = document.getElementById("signup")

const USER_FIRST_NAME_MIN = 2
const USER_FIRST_NAME_MAX = 20

const USER_LAST_NAME_MIN = 2
const USER_LAST_NAME_MAX = 20

const USER_PASSWORD_MIN = 8
const USER_PASSWORD_MAX = 50

window.addEventListener("load", ()=>{
console.log("I WAS HIDING!")
console.log("WHAT AM I?!: ",USER_FIRST_NAME_MIN,"and? ",USER_FIRST_NAME_MAX)

user_first_name.addEventListener("input", ()=>{
    if (user_first_name.value.length < USER_FIRST_NAME_MIN) {
        user_first_name.classList = ""
        user_first_name.classList.add("error")
    } else if (user_first_name.value.length > USER_FIRST_NAME_MAX) {
        user_first_name.classList = ""
        user_first_name.classList.add("error")
    }else {
        user_first_name.classList = ""
        user_first_name.classList.add("ok")
    }
})
user_last_name.addEventListener("input", ()=>{
    if (user_last_name.value.length < USER_LAST_NAME_MIN) {
        user_last_name.classList = ""
        user_last_name.classList.add("error")
    } else if (user_last_name.value.length > USER_LAST_NAME_MAX) {
        user_last_name.classList = ""
        user_last_name.classList.add("error")
    }else {
        user_last_name.classList = ""
        user_last_name.classList.add("ok")
    }
})

user_password.addEventListener("input", ()=>{
    if (user_password.value.length < USER_PASSWORD_MIN) {
        user_password.classList = ""
        user_password.classList.add("error")
    } else if (user_password.value.length > USER_PASSWORD_MAX) {
        user_password.classList = ""
        user_password.classList.add("error")
    }else {
        user_password.classList = ""
        user_password.classList.add("ok")
    }
})

})