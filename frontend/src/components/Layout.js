 
import Navbar from './Navbar';

const Layout = ({ children }) => {
    return (
        <>
            <Navbar />
            <main>
                <div className="container">
                    {children}
                </div>
            </main>
        </>
    );
};

export default Layout;