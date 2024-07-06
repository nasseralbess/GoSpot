import logo from "../images/logo.png"
const Nav = ({authToken}) => {
    return (
        <nav>  

            <div className="logo_container"> 
             <img className="logo" src={logo} />

            </div>


            {!authToken && (  
                <button className="nav-button"  >
                    Log in
                </button>
            )}
        </nav>
      
    )
  }
  export default Nav