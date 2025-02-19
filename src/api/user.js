import api from "./request.js";


export function userLogin(data) {
  return api.post('user/login', data)
}

export function userRegister(data) {
  return api.post('user', data)
}

export function userChangePassword(data) {
  return api.put('user', data)
}

export function userCaptcha(email, data) {
  return api.get(`user/captcha/${email}`, {
    params: data
  })
}

// export function userLogin(data){
//   return api.post('user/login')
// }
