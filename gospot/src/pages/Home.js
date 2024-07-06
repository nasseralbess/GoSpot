import Nav from "../components/Nav.js"
import AuthModel from "../components/AuthModel.js"
import { useState } from "react" 
const Home = () => {

  const [showModel, setShowModel] = useState(false)

  const authToken = false

  const handleClick = () => {
    console.log('clicked');
    setShowModel(true); // Corrected the typo here
  };
  return (
    
   
    <div className="overlay">
      <Nav authToken={authToken}/>
      <h1>Swipe Right </h1>
      <button className="primary_button" onClick={handleClick}>
        {authToken ? "Signout" : "Create Account"}
      </button>

      {showModel && (
        <AuthModel setShowModel = {setShowModel}/>
      )}

    </div>

  
  )
}
export default Home