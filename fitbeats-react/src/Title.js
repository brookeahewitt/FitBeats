import React from 'react';
import { Container, Nav, Navbar, NavbarToggle, NavbarCollapse } from 'react-bootstrap';


function Title() {
  return (
    <Navbar collapseOnSelect expand="lg" bg="dark" variant="dark">
      <Container>
        <NavbarToggle aria-controls='responsive-navbar-nav' />
        <NavbarCollapse id='responsive-navbar-nav'>
          <Nav>
            <Nav.Link href='/generate'>Generate</Nav.Link>
            <Nav.Link href='/explore'>Explore</Nav.Link>
            <Nav.Link href='/activity'>Activity</Nav.Link>
            <Nav.Link href='/info'>Info</Nav.Link>
          </Nav>
        </NavbarCollapse>
      </Container>
    </Navbar>
  );
}

export default Title;
