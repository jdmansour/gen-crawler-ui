// import * as React from 'react';
import { Button, IconButton, Link, Menu, MenuItem, Paper, Typography } from '@mui/material';
import { createTheme, styled, ThemeProvider } from '@mui/material/styles';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import { crawlerList } from "./data";
import { defaultTheme, roundedTheme } from "./TableTest";
import MoreVertIcon from '@mui/icons-material/MoreVert';
import React from 'react';

export default function CrawlerTable(props: { theme?: 'default' | 'rounded' }) {
    const { theme } = props;
    const appliedTheme = theme === 'rounded' ? roundedTheme : defaultTheme;
    const rows = crawlerList;
    const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);
    const open = Boolean(anchorEl);
    const handleClick = (event: React.MouseEvent<HTMLButtonElement>) => {
        setAnchorEl(event.currentTarget);
    };
    const handleClose = () => {
        setAnchorEl(null);
    };
    return (
        <ThemeProvider theme={appliedTheme}>
            <Menu
                id="basic-menu"
                anchorEl={anchorEl}
                anchorOrigin={{ vertical: 'top', horizontal: 'left' }}
                transformOrigin={{ vertical: 'top', horizontal: 'right' }}
                // anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
                // transformOrigin={{ vertical: 'top', horizontal: 'right' }}
                open={open}
                onClose={handleClose}
                slotProps={{
                list: {
                    'aria-labelledby': 'basic-button',
                },
                }}
            >
                <MenuItem onClick={handleClose}>Profile</MenuItem>
                <MenuItem onClick={handleClose}>My account</MenuItem>
                <MenuItem onClick={handleClose}>Logout</MenuItem>
            </Menu>
            <TableContainer component={Paper}>
                <Table>
                    {/* <TableHead>
                        <TableRow>
                            <TableCell>Name</TableCell>
                            <TableCell>Status</TableCell>
                            <TableCell>Last Updated</TableCell>
                            <TableCell></TableCell>
                        </TableRow>
                    </TableHead> */}
                    <TableBody>
                        {rows.map((row) => (
                            <TableRow key={row.name}>
                                <TableCell component="th" scope="row">
                                    <Typography fontSize={20}><Link href="#">{row.name}</Link></Typography>
                                </TableCell>
                                <TableCell>
                                    <Typography variant='body2' color='textSecondary'>Status</Typography>
                                    {row.status}
                                </TableCell>
                                <TableCell>
                                    <Typography variant='body2' color='textSecondary'>Last Updated</Typography>
                                    {row.updatedAt.toISOString()}
                                </TableCell>
                                <TableCell align="right">
                                    {/* Button with the vertical ellipsis icon */}
                                    <IconButton  id="basic-button"
                                        aria-controls={open ? 'basic-menu' : undefined}
                                        aria-haspopup="true"
                                        aria-expanded={open ? 'true' : undefined}
                                        onClick={handleClick}>
                                        <MoreVertIcon />
                                    </IconButton>
                                </TableCell>
                                {/* <TableCell>{row.protein}</TableCell> */}
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
        </ThemeProvider>
    );
}
