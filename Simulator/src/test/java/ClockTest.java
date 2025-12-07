import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.awt.*;
import java.io.IOException;

import static org.junit.jupiter.api.Assertions.*;

public class ClockTest
{
    private Clock clock;
    private DrawingApp app;

    @BeforeEach
    void setup() throws IOException
    {
        app = new DrawingApp();
        clock = new Clock("C1", new Rectangle(0, 0, 100, 100), Color.YELLOW,
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
        assertTrue(clock.hasOutput());
        assertFalse(clock.hasInput());
    }

    @Test
    void testToStringContainsClock()
    {
        assertTrue(clock.toString().contains("pysim.clock"));
    }

    @Test
    void testBlockType()
    {
        assertEquals("Clock", clock.getType());
    }
}
