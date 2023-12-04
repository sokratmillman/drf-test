import { useState } from "react"
import { Link, useNavigate } from "react-router-dom"

export default function RegisterPage() {
    const [validationError, setValidateionError] = useState(false)
    const [uniqueUser, setUniqueUser] = useState(true)
    const navigate = useNavigate()


    function validate(userform) {
        if (userform['password'] !== userform['password2']) {
            return false
        }
        return true
    }
    function handleSubmit(event) {
        event.preventDefault()
        const userForm = {}
        const formData = new FormData(event.currentTarget)
        formData.forEach((value, property) => {
            userForm[property] = value
        })
        if (validate(userForm)) {
            setValidateionError(false)
        } else {
            setValidateionError(true)
            return
        }
        const body = {"username": userForm['username'], "password": userForm['password']}

        fetch("http://127.0.0.1:8000/registration/register/", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(body)

        }).then((res) => {
            res = res.json()
            return res
        }).then((res) => {
            if (res.status === 201) {
                navigate("/login")
            } else {
                setUniqueUser((uniqueUser) => {
                    return res.data['username'][0] === "A user with that username already exists." ? false : true
                })
            }
        })

    }
    return (
    <>
    <h1>Регистрация</h1>
        {validationError && <h2 style={{"color":"red"}}>Пароли не совпадают</h2>}
        {!uniqueUser && <h2 style={{"color":"red"}}>Такой логин уже занят</h2>}
        <form onSubmit={handleSubmit}>
            <input type="text" placeholder="username" id="username" name="username"/>
            <label htmlFor="username">Логин</label>
            <input type="password" placeholder="пароль" id="password" name="password"/>
            <label htmlFor="password">Пароль</label>
            <input type="password" placeholder="Повторите пароль" id="password2" name="password2"/>
            <label htmlFor="password2">Повторите пароль</label>
            <button type="submit">Зарегистрироваться</button>
        </form>
        <Link to="/login">Уже есть аккаунт</Link>
    </>
    )
}