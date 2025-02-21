import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from './dashboard/Home'; // Import your Home component
import Dashboard from './Dashboard'; // Import your Dashboard component

function App() {
    return (
        <Router>
            <Routes>
                {/* Home page */}
                <Route path="/" element={<Home />} />

                {/* Dashboard page */}
                <Route path="/dashboard" element={<Dashboard />} />
            </Routes>
        </Router>
    );
}

export default App;
