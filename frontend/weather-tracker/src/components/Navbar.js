import {Link} from "react-router-dom"
import React from "react"
import logo from '../images/logo.png';

export default function Navbar() {

    return (
        <nav>
            <img src={logo} className="nav--logo"/>
            <div>
                <input list="countries" className="nav--search" placeholder="Search Country"></input>
                <Link to="/country">
                    <button>Search</button>
                </Link>
            </div>
            <div>
                <Link to="/account">
                    <button className="nav--button">Sign In</button>
                </Link>
                <Link to="/account">
                    <button className="nav--button">Log In</button>
                </Link>
            </div>
        </nav>
    )
}