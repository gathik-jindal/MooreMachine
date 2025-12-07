import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.awt.*;
import java.io.IOException;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

public class MealyTest
{
    private Mealy mealy;
    private DrawingApp app;

    @BeforeEach
    void setup() throws IOException
    {
        app = new DrawingApp();
        mealy = new Mealy("M2", new Rectangle(0, 0, 100, 100), Color.BLUE,
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
    void testToStringContainsMealy()
    {
        assertTrue(mealy.toString().contains("pysim.mealy"));
    }

    @Test
    void testBlockType()
    {
        assertEquals("Mealy", mealy.getType());
    }

    @Test
    void testHasInputOutput()
    {
        assertTrue(mealy.hasInput());
        assertTrue(mealy.hasOutput());
    }
}
