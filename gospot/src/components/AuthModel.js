const AuthModel = ({setShowModel}) => {

    const handleClick = () => {
        setShowModel(false)

    }
    return (
      <div> 
        <div onClick = {handleClick}>
            X
        </div>
      </div>
    )
  }
  export default AuthModel