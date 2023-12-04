import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import Header from "../components/Header";

const BASE_URL = "http://127.0.0.1:8000"

function TestPage() {
    const [testData, setTestData] = useState("")
    const urlparams = useParams()
    const navigate = useNavigate()


    useEffect(() => {
        if (!sessionStorage.getItem("token")) {
          navigate("/login")
        }
        const token = sessionStorage.getItem("token")
        const testid = urlparams.testid
        fetch(`${BASE_URL}/test/${testid}/`, {
            method: "GET",
      
            headers: {
              "Content-Type": "application/json",
              Authorization: token,
            },
          }).then((res)=> {
            if (res.status === 401) {
              navigate("/login")
              return
            } else if (res.status === 423) {
              navigate(`/test/${testid}/results/`)
              return
            } else {
              res = res.json()
              return res
            }
          }).then((res)=>{
            setTestData(res.data)
          }).catch((rej) => {
            
          })
    }, [])

    function handleSubmit(event) {
      event.preventDefault();
      const testid = urlparams.testid
      const token = sessionStorage.getItem("token")
      const body = {};
      const data = new FormData(event.currentTarget);
      data.forEach((value, property) => {
        if (body[property]) {
          body[property].push(value);
        } else {
          body[property] = [value];
        }
      });
  
      fetch(`http://localhost:8000/test/${testid}/`, {
        method: "POST",
  
        headers: {
          "Content-Type": "application/json",
          Authorization: token,
        },
        body: JSON.stringify(body),
      }).then((res) => {
        if (res.status == 201) {
          navigate(`/test/${testid}/results/`)
        }
      });
    }
  
    return (
      <>
        <Header/>
        {testData.test_name ? <><h1>{testData.test_name}</h1>
        <form onSubmit={handleSubmit}>
          {testData.questions.map((question) => {
            if (question.question_type === "SC") {
              return (
                <div>
                  <h2>{question.question_text}</h2>
                  {question.choices.map((option) => {
                    return (
                      <>
                        <input
                          type="radio"
                          name={option.question}
                          id={option.choice_text}
                          value={option.choice_text}
                        />
                        <label htmlFor={option.choice_text}>{option.choice_text}</label>
                      </>
                    );
                  })}
                </div>
              );
            } else {
              return (
                <div>
                  <h2>{question.question_text}</h2>
                  {question.choices.map((option) => {
                    return (
                      <>
                        <input
                          type="checkbox"
                          name={option.question}
                          id={option.choice_text}
                          value={option.choice_text}
                        />
                        <label htmlFor={option.choice_text}>{option.choice_text}</label>
                      </>
                    );
                  })}
                </div>
              );
            }
          })}
          <button type="submit">Submit</button>
        </form></> : <h1>Loading test</h1>}
        
      </>
    );
  }

export default TestPage