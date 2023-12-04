import { useState } from "react"
import { Link, useNavigate } from "react-router-dom"

export default function LoginPage() {
    const [validationError, setValidateionError] = useState(false)
    const navigate = useNavigate()
    
    function handleSubmit(event) {
        event.preventDefault()
        const userForm = {}
        const formData = new FormData(event.currentTarget)
        formData.forEach((value, property) => {
            userForm[property] = value
        })

        fetch("http://127.0.0.1:8000/registration/login/", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userForm)

        }).then((res) => {
            res = res.json()
            return res
        }).then((res) => {
            if (res.status === 401) {
                setValidateionError(true)
            } else if (res.status === 200) {
                const token = `Token ${res.data.Token}`
                sessionStorage.setItem("token", token)
                navigate("/")
            }
        })

    }
    return (
    <>
    <h1>Вход в аккаунт</h1>
        {validationError && <h2 style={{"color":"red"}}>Неверный логин или пароль</h2>}
        <form onSubmit={handleSubmit}>
            <input type="text" placeholder="username" id="username" name="username"/>
            <label htmlFor="username">Логин</label>
            <input type="password" placeholder="пароль" id="password" name="password"/>
            <label htmlFor="password">Пароль</label>
            <button type="submit">Войти</button>
        </form>
        <Link to="/register">Создать аккаунт</Link>
    </>
    )
}