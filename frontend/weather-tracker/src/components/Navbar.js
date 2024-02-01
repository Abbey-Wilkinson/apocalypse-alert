import {Link, Navigate} from "react-router-dom"
import React from "react"
import logo from '../images/apocalyse_alert_logo.png';

export default function Navbar() {
    const [country, setCountry] = React.useState(" ")
    const [calledData, setCalledData] = React.useState(false)

    function handleChange(event) {
        setCountry(event.target.value)
    }

    function checkCountry() {
        console.log("called")
        fetch("http://localhost:3000/check?country=" + country)
            .then(res => res.json())
            .then(data => setCalledData(data.found))
    }

    React.useEffect(() => {checkCountry()}, [])

    if (calledData) {
        return <Navigate to={`/country/${country}`}/>
    }

    return (
        <nav>
            <img src={logo} className="nav--logo"/>
            <div>
                <input className="nav--search" placeholder="Search Country" onChange={handleChange}/>
                <button className="nav--search-button" onClick={checkCountry}>Search</button>
            </div>
            <div>
                <Link to="/account">
                    <button className="nav--account-button">Sign In</button>
                </Link>
                <Link to="/account">
                    <button className="nav--account-button">Log In</button>
                </Link>
            </div>
        </nav>
    )
}