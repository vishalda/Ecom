import {API} from "../../backend";

export const getmeToken = (userId, token) => {
    return fetch(`${API}payment/gettoken/${userId}/${token}/`,{
        method:"GET",
    })
    .then((response) => {
        console.log("HELLo");
        return response.json();
    })
    .catch(error => console.log(error));
};


export const processPayment = (userId, token, paymentInfo) =>{
    console.log("Succes")
    const formData = new FormData();
    for(const name in paymentInfo){
        formData.append(name, paymentInfo[name])
    }
    return fetch(`${API}payment/process/${userId}/${token}/`,{
        method:"POST",
        body: formData
    })
    .then(response =>{
        console.log("p-0",response);
        return response.json();
    })
    .catch(err => console.log("Error",err))
}