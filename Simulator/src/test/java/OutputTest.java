import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.awt.*;
import java.io.IOException;

import static org.junit.jupiter.api.Assertions.*;

public class OutputTest
{
    private Output output;
    private DrawingApp app;

    @BeforeEach
    void setup() throws IOException
    {
        app = new DrawingApp();
        output = new Output("O1", new Rectangle(0, 0, 100, 100), Color.MAGENTA,
                app.getManager().getDrawCircuit());
    }

    @AfterEach
    void close()
    {
        if (app != null)
        {
            javax.swing.SwingUtilities.invokeLater(() -> app.dispose());
        }
    }

    @Test
    void testHasOnlyInput()
    {
        assertFalse(output.hasOutput());
        assertTrue(output.hasInput());
    }

    @Test
    void testToStringContainsOutput()
    {
        assertTrue(output.toString().contains("pysim.output"));
    }

    @Test
    void testBlockType()
    {
        assertEquals("Output Block", output.getType());
    }
}
