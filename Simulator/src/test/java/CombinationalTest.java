import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.awt.*;
import java.io.IOException;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

public class CombinationalTest
{
    private Combinational comb;
    private DrawingApp app;

    @BeforeEach
    void setup() throws IOException
    {
        app = new DrawingApp();
        comb = new Combinational("C1", new Rectangle(0, 0, 100, 100), Color.CYAN,
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
    void testHasInputOutput()
    {
        assertTrue(comb.hasInput());
        assertTrue(comb.hasOutput());
    }

    @Test
    void testToStringContainsCombinational()
    {
        assertTrue(comb.toString().contains("pysim.combinational"));
    }

    @Test
    void testBlockType()
    {
        assertEquals("Combinational Block", comb.getType());
    }
}
