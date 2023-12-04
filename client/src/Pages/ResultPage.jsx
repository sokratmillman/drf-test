import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import Header from "../components/Header";

const BASE_URL = "http://127.0.0.1:8000"

export default function ResultPage() {
    const [resultData, setResultData] = useState("")
    const urlparams = useParams()
    const navigate = useNavigate()

    useEffect(() => {
        if (!sessionStorage.getItem("token")) {
            navigate("/login")
        } 
        const token = sessionStorage.getItem("token")
        const testid = urlparams.testid
        fetch(`${BASE_URL}/test/${testid}/results/`, {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
              Authorization: token,
            },
          }).then((res)=> {
            res = res.json()
            return res
          }).then((res)=>{
            setResultData(res.data)
          })
    }, [])

    return (
      resultData && <>
        <Header/>
        <h1>{resultData.test_name}</h1>
        {resultData.result_string.split("|||").map((answer)=> {
            return <p>{answer}</p>
        })}
      </>
    );
  }