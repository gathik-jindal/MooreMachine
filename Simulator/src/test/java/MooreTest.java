import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.awt.*;
import java.io.IOException;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

public class MooreTest
{
    private Moore moore;
    private DrawingApp app;

    @BeforeEach
    void setup() throws IOException
    {
        app = new DrawingApp();
        moore = new Moore("M1", new Rectangle(0, 0, 100, 100), Color.RED, app.getManager().getDrawCircuit());
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
    void testDefaultMaxOutSize()
    {
        assertEquals(1, moore.getMaxOutSize());
    }

    @Test
    void testStartingStateDefault()
    {
        assertEquals(0, moore.getStartingState());
    }

    @Test
    void testToStringContainsName()
    {
        assertTrue(moore.toString().contains("pysim.moore"));
    }

    @Test
    void testBlockType()
    {
        assertEquals("Moore", moore.getType());
    }

    @Test
    void testHasInputOutput()
    {
        assertTrue(moore.hasInput());
        assertTrue(moore.hasOutput());
    }
}
