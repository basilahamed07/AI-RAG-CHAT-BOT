// src/components/chat_bot/Sidebar.js
import React from "react";
import { Link } from "react-router-dom";
import { Drawer, List, ListItem, ListItemText } from "@mui/material";

const Sidebar = () => {
  return (
    <Drawer
      sx={{
        width: 240,
        flexShrink: 0,
        "& .MuiDrawer-paper": {
          width: 240,
          boxSizing: "border-box",
        },
      }}
      variant="permanent"
      anchor="left"
    >
      <List>
        <ListItem button component={Link} to="/chat/chat-history">
          <ListItemText primary="Chat History" />
        </ListItem>
        {/* Add more links to other chat-related views here */}
      </List>
    </Drawer>
  );
};

export default Sidebar;
