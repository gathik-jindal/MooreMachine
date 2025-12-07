import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.awt.*;
import java.io.IOException;

import static org.junit.jupiter.api.Assertions.*;

public class InputTest
{
    private Input input;
    private DrawingApp app;

    @BeforeEach
    void setup() throws IOException
    {
        app = new DrawingApp();
        input = new Input("I1", new Rectangle(0, 0, 100, 100), Color.BLACK,
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
    void testHasOnlyOutput()
    {
        assertTrue(input.hasOutput());
        assertFalse(input.hasInput());
    }

    @Test
    void testToStringContainsSource()
    {
        assertTrue(input.toString().contains("pysim.source"));
    }

    @Test
    void testBlockType()
    {
        assertEquals("Input Block", input.getType());
    }
}
