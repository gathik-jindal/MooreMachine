import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.awt.*;
import java.awt.geom.Line2D;
import java.io.IOException;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;

public class WireTest
{
    private DrawingApp app;

    @BeforeEach
    void setup() throws IOException
    {
        app = new DrawingApp();
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
    void testWireConnection()
    {
        Input input = new Input("I1", new Rectangle(), Color.BLACK,
                app.getManager().getDrawCircuit());

        Output output = new Output("O1", new Rectangle(), Color.BLACK,
                app.getManager().getDrawCircuit());

        Wire wire = new Wire("W1",
                new Line2D.Double(0, 0, 100, 100),
                Color.BLACK,
                app.getManager().getDrawCircuit());

        wire.setBlock(input);
        wire.setBlock(output);

        assertEquals(input, wire.getStartBlock());
        assertEquals(output, wire.getEndBlock());
    }

    @Test
    void testArrowHeadExists()
    {
        Wire wire = new Wire("W2",
                new Line2D.Double(0, 0, 50, 50),
                Color.BLACK,
                app.getManager().getDrawCircuit());

        assertNotNull(wire.getArrowHead());
    }
}
