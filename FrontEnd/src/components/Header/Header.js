import Container from "react-bootstrap/Container";
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";
import NavDropdown from "react-bootstrap/NavDropdown";

function Header() {
  return (
    <Navbar
      fixedTop
      style={{
        backgroundSize: "0",
        backgroundColor: "#fdd26d",
        height: "100px",
      }}
    >
      <Container fluid>
        <h1 className="title-text">ANN</h1>
        <Navbar.Toggle />
        <Navbar.Collapse className="justify-content-end">
          <Navbar.Text>
            <button className="btn dtn-default">Login</button>
          </Navbar.Text>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}

export default Header;
