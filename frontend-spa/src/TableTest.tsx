import Paper from '@mui/material/Paper';
import { createTheme, styled, ThemeProvider } from '@mui/material/styles';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';

export const defaultTheme = createTheme();

export const roundedTheme = createTheme({
    // palette: {
    //     primary: {
    //         main: '#1976d2',
    //     },
    // },
    typography: {
        fontFamily: 'Montserrat, Arial, sans-serif',
        fontWeightRegular: 500,
    },
    components: {
        MuiTableContainer: {
            styleOverrides: {
                'root': {
                    boxShadow: 'none',
                    backgroundColor: 'transparent',
                    padding: '0px',
                }
            }
        },
        MuiTable: {
            styleOverrides: {
                'root': {
                    borderCollapse: 'separate',
                    borderSpacing: '0px 1px',
                    padding: '5px',
                }
            }
        },
        MuiTableRow: {
            styleOverrides: {
                'root': ({ theme }) => ({
                    position: 'relative',
                    zIndex: '10',
                    backgroundColor: 'transparent',
                    "&::after": {
                        content: '""',
                        position: "absolute",
                        left: 0,
                        top: 0,
                        right: 0,
                        bottom: 0,
                        zIndex: -1,
                        backgroundColor: "white",
                        boxShadow: theme.shadows[2],
                        borderRadius: "12px",
                    },
                }),
            },
        },
        MuiTableCell: {
            styleOverrides: {
                'root': {
                    border: 0,
                }
            }
        }
    }
});

const StyledTable = styled(Table)(({ theme }) => ({
    // color: 'red',
    // border: '1px solid orange',
    borderCollapse: 'separate',
    borderSpacing: '0px 1px',
    padding: '5px',
}));

const StyledTableCell = styled(TableCell)(({ theme }) => ({
    border: 0,
    // [`&.${tableCellClasses.head}`]: {
    //   backgroundColor: theme.palette.common.black,
    //   color: theme.palette.common.white,
    // },
    // [`&.${tableCellClasses.body}`]: {
    //   fontSize: 14,
    // },
}));

const StyledTableRow = styled(TableRow)(({ theme }) => ({
    position: 'relative',
    zIndex: '10',
    backgroundColor: 'transparent',
    '&:after': {
        content: '""',
        position: 'absolute',
        left: 0,
        top: 0,
        right: 0,
        bottom: 0,
        zIndex: -1,
        backgroundColor: 'white',
        boxShadow: theme.shadows[2],
        borderRadius: '12px',
    },
}));

function createData(
    name: string,
    calories: number,
    fat: number,
    carbs: number,
    protein: number,
) {
    return { name, calories, fat, carbs, protein };
}

const rows = [
    createData('Frozen yoghurt', 159, 6.0, 24, 4.0),
    createData('Ice cream sandwich', 237, 9.0, 37, 4.3),
    createData('Eclair', 262, 16.0, 24, 6.0),
    createData('Cupcake', 305, 3.7, 67, 4.3),
    createData('Gingerbread', 356, 16.0, 49, 3.9),
];

export default function TableTest(props: { theme?: 'default' | 'rounded' }) {
    const { theme } = props;
    const appliedTheme = theme === 'rounded' ? roundedTheme : defaultTheme;

    return (
        <ThemeProvider theme={appliedTheme}>
            <TableContainer component={Paper}>
                <Table sx={{ minWidth: 700 }}>
                    <TableHead>
                        <TableRow>
                            <TableCell>Dessert (100g serving)</TableCell>
                            <TableCell align="right">Calories</TableCell>
                            <TableCell align="right">Fat&nbsp;(g)</TableCell>
                            <TableCell align="right">Carbs&nbsp;(g)</TableCell>
                            <TableCell align="right">Protein&nbsp;(g)</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {rows.map((row) => (
                            <TableRow key={row.name}>
                                <TableCell component="th" scope="row">
                                    {row.name}
                                </TableCell>
                                <TableCell align="right">{row.calories}</TableCell>
                                <TableCell align="right">{row.fat}</TableCell>
                                <TableCell align="right">{row.carbs}</TableCell>
                                <TableCell align="right">{row.protein}</TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
        </ThemeProvider>
    );
}
