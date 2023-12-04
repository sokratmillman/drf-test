import { useEffect, useState } from "react"
import { Link, useNavigate } from "react-router-dom"

export default function DashboardPage() {
    const navigate = useNavigate()
    const [testItems, setTestItems] = useState([])
    const [resultItems, setResultItems] = useState([])
    useEffect(()=>{
        if (!sessionStorage.getItem("token")) {
            navigate("/login")
        } else {
            const token = sessionStorage.getItem("token")
            fetch(`http://127.0.0.1:8000/`, {
                method: "GET",
                headers: {
                  "Content-Type": "application/json",
                  Authorization: token,
                },
              }).then((res) => {
                res = res.json()
                return res
              }).then((res) => {
                if (res.status === 200) {
                    const data = res.data
                    data.forEach(element => {
                        if (element['is_available']) {
                            setTestItems((testItems) => [...testItems, element])
                        } else {
                            setResultItems((resultItems) => [...resultItems, element])
                        }
                    });
                }
              })
        }
    }, [])

    return (
        <div style={{"display": "flex", "flexDirection": "column"}}>
            <button type="button" onClick={()=> {sessionStorage.removeItem("token"); navigate("/login")}}>Выйти</button>
            <h1>Все тесты и результаты</h1>
            <h2>Тесты, доступные для прохождения</h2>
            {testItems.map((test) => {
                return (
                    <>
                        <div key={test.test_name} style={{"border": "5px solid black", "margin": "10px"}}>
                            <h3 style={{"color": "blue"}}>{test['test_name']}</h3>
                            <Link to={`/test/${test.id}`}>Пройти тест</Link>
                        </div>
                    </>
                )
            })}
            <h2>Результаты</h2>
            {resultItems.map((test) => {
                return (
                    <>
                        <div key={test.test_name} style={{"border": "5px solid black", "margin": "10px"}}>
                            <h3 style={{"color": "grey"}}>{test['test_name']}</h3>
                            <Link to={`/test/${test.id}/results`}>Посмотреть результаты</Link>
                        </div>
                    </>
                )
            })}
        </div>
        
    )
}