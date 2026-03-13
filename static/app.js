


window.addEventListener("load", ()=>{
const user_first_name = document.getElementById("user_first_name");
const user_last_name = document.getElementById("user_last_name");
const user_password = document.getElementById("user_password");

const USER_FIRST_NAME_MIN = document.getElementById("USER_FIRST_NAME_MIN").textContent
const USER_FIRST_NAME_MAX = document.getElementById("USER_FIRST_NAME_MAX").textContent

const USER_LAST_NAME_MIN = document.getElementById("USER_LAST_NAME_MIN").textContent
const USER_LAST_NAME_MAX = document.getElementById("USER_LAST_NAME_MAX").textContent

const USER_PASSWORD_MIN = document.getElementById("USER_PASSWORD_MIN").textContent
const USER_PASSWORD_MAX = document.getElementById("USER_PASSWORD_MAX").textContent

user_first_name?.addEventListener("input", ()=>{
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
user_last_name?.addEventListener("input", ()=>{
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

user_password?.addEventListener("input", ()=>{
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


// #######################################

// #               Travels               #

// #######################################

const travel_title = document.getElementById("travel_title");
const travel_description = document.getElementById("travel_description");
const travel_location = document.getElementById("travel_location");
const travel_country = document.getElementById("travel_country");

const travel_date_from = document.getElementById("travel_date_from");
const travel_date_to = document.getElementById("travel_date_to");

const TRAVEL_TITLE_MIN = document.getElementById("TRAVEL_TITLE_MIN").textContent
const TRAVEL_TITLE_MAX = document.getElementById("TRAVEL_TITLE_MAX").textContent

const TRAVEL_DESCRIPTTION_MIN = document.getElementById("TRAVEL_TITLE_MIN").textContent
const TRAVEL_DESCRIPTTION_MAX = document.getElementById("TRAVEL_TITLE_MAX").textContent

const TRAVEL_LOCATION_MIN = document.getElementById("TRAVEL_TITLE_MIN").textContent
const TRAVEL_LOCATION_MAX = document.getElementById("TRAVEL_TITLE_MAX").textContent

const TRAVEL_COUNTRY_MIN = document.getElementById("TRAVEL_TITLE_MIN").textContent
const TRAVEL_COUNTRY_MAX = document.getElementById("TRAVEL_TITLE_MAX").textContent


travel_title?.addEventListener("input", ()=>{
    if (travel_title.value.length < TRAVEL_TITLE_MIN) {
        travel_title.classList = ""
        travel_title.classList.add("error")
    } else if (travel_title.value.length > TRAVEL_TITLE_MAX) {
        travel_title.classList = ""
        travel_title.classList.add("error")
    }else {
        travel_title.classList = ""
        travel_title.classList.add("ok")
    }
})
travel_description?.addEventListener("input", ()=>{
    if (travel_description.value.length < TRAVEL_DESCRIPTTION_MIN) {
        travel_description.classList = ""
        travel_description.classList.add("error")
    } else if (travel_description.value.length > TRAVEL_DESCRIPTTION_MAX) {
        travel_description.classList = ""
        travel_description.classList.add("error")
    }else {
        travel_description.classList = ""
        travel_description.classList.add("ok")
    }
})

travel_location?.addEventListener("input", ()=>{
    if (travel_location.value.length < TRAVEL_LOCATION_MIN) {
        travel_location.classList = ""
        travel_location.classList.add("error")
    } else if (travel_location.value.length > TRAVEL_LOCATION_MAX) {
        travel_location.classList = ""
        travel_location.classList.add("error")
    }else {
        travel_location.classList = ""
        travel_location.classList.add("ok")
    }
})

travel_country?.addEventListener("input", ()=>{
    if (travel_country.value.length < TRAVEL_COUNTRY_MIN) {
        travel_country.classList = ""
        travel_country.classList.add("error")
    } else if (travel_country.value.length > TRAVEL_COUNTRY_MAX) {
        travel_country.classList = ""
        travel_country.classList.add("error")
    }else {
        travel_country.classList = ""
        travel_country.classList.add("ok")
    }
})

})