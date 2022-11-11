import { useState } from 'react';
import axios from "axios";

function Login(props) {

    const [loginForm, setloginForm] = useState({
      email: "",
      password: ""
    })

    function logMeIn(event) {
      axios({
        method: "POST",
        url:"/api/token",
        data:{
          email: loginForm.email,
          password: loginForm.password
         }
      })
      .then((response) => {
        props.setToken(response.data.access_token)
      }).catch((error) => {
        if (error.response) {
          console.log(error.response)
          console.log(error.response.status)
          console.log(error.response.headers)
          }
      })

      setloginForm(({
        email: "",
        password: ""}))

      event.preventDefault()
    }

    function loginHandleChange(event) {
      const {value, name} = event.target
      setloginForm(prevNote => ({
          ...prevNote, [name]: value})
      )}

    const [signupForm, setSignupForm] = useState({
      email: "",
      password: ""
    })

    function signMeUp(event) {
      axios({
        method: "POST",
        url:"/api/signup",
        data:{
          email: signupForm.email,
          password: signupForm.password
         }
      })
      .then((response) => {
        props.setToken(response.data.access_token)
      }).catch((error) => {
        if (error.response) {
          console.log(error.response)
          console.log(error.response.status)
          console.log(error.response.headers)
          }
      })

      setSignupForm(({
        email: "",
        password: ""}))

      event.preventDefault()
    }

    function signupHandleChange(event) {
      const {value, name} = event.target
      setSignupForm(prevNote => ({
          ...prevNote, [name]: value})
      )}

    return (
      <div>
        <h1>Login</h1>
          <form className="login">
            <input onChange={loginHandleChange}
                  type="email"
                  text={loginForm.email}
                  name="email"
                  placeholder="Email"
                  value={loginForm.email} />
            <input onChange={loginHandleChange}
                  type="password"
                  text={loginForm.password}
                  name="password"
                  placeholder="Password"
                  value={loginForm.password} />

          <button onClick={logMeIn}>Submit</button>
        </form>

        <h1>Sign Up</h1>
          <form className="signup">
            <input onChange={signupHandleChange}
                  type="email"
                  text={signupForm.email}
                  name="email"
                  placeholder="Email"
                  value={signupForm.email} />
            <input onChange={signupHandleChange}
                  type="password"
                  text={signupForm.password}
                  name="password"
                  placeholder="Password"
                  value={signupForm.password} />

          <button onClick={signMeUp}>Submit</button>
        </form>
      </div>
    );
}

export default Login;