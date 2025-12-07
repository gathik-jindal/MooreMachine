import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.awt.*;
import java.awt.geom.Line2D;
import java.io.IOException;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class FullIntegrationTest
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
    void testInputToMooreToOutputFlow()
    {
        Input input = new Input("Input1", new Rectangle(), Color.BLACK,
                app.getManager().getDrawCircuit());

        Moore moore = new Moore("Moore1", new Rectangle(), Color.RED,
                app.getManager().getDrawCircuit());

        Output output = new Output("Output1", new Rectangle(), Color.BLUE,
                app.getManager().getDrawCircuit());

        Wire w1 = new Wire("W1", new Line2D.Double(0, 0, 50, 50),
                Color.BLACK, app.getManager().getDrawCircuit());

        Wire w2 = new Wire("W2", new Line2D.Double(50, 50, 100, 100),
                Color.BLACK, app.getManager().getDrawCircuit());

        w1.setBlock(input);
        w1.setBlock(moore);

        w2.setBlock(moore);
        w2.setBlock(output);

        assertEquals(input, w1.getStartBlock());
        assertEquals(moore, w1.getEndBlock());

        assertEquals(moore, w2.getStartBlock());
        assertEquals(output, w2.getEndBlock());
    }
}
