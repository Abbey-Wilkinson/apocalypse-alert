import logo from '../maybe.png';

export default function Navbar() {
    return (
        <nav>
            <img src={logo} className="nav--logo"/>
            <input className="nav--search" placeholder="Search Country"></input>
            <div className="nav--buttons">
                <button>Sign In</button>
                <button>Log In</button>
            </div>
        </nav>
    )
}