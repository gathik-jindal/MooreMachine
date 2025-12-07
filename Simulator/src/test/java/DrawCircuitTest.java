import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.awt.*;
import java.awt.geom.Line2D;
import java.awt.image.BufferedImage;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Tests real rendering of a block in DrawCircuit
 */
public class DrawCircuitTest
{

    private DrawCircuit drawCircuit;

    @BeforeEach
    void setup() throws Exception
    {
        DrawingApp drawingApp = new DrawingApp();
        Manager manager = drawingApp.getManager();
        drawCircuit = manager.getDrawCircuit();
    }

    // MAIN TEST: Block is drawn and verified by pixel color
    @Test
    void testBlockIsRenderedOnScreen()
    {
        // Arrange: Inject fake block manually
        Rectangle rect = new Rectangle(50, 50, 100, 100);
        Block block = new Moore("TEST", rect, Color.BLUE, drawCircuit);

        drawCircuit.getRectangles().add(block);

        // Render to offscreen image
        BufferedImage image = new BufferedImage(300, 300, BufferedImage.TYPE_INT_RGB);
        Graphics2D g2 = image.createGraphics();
        drawCircuit.paint(g2);
        g2.dispose();

        // Assert INSIDE pixel is blue
        int insidePixel = image.getRGB(75, 75);
        assertEquals(Color.BLUE.getRGB(), insidePixel);

        // Assert OUTSIDE pixel is NOT blue
        int outsidePixel = image.getRGB(10, 10);
        assertNotEquals(Color.BLUE.getRGB(), outsidePixel);
    }

    // Logic test: Intersection detection
    @Test
    void testRectangleIntersectionDetection()
    {
        Rectangle r1 = new Rectangle(50, 50, 100, 100);
        Rectangle r2 = new Rectangle(80, 80, 40, 40);

        Block block = new Moore("A", r1, Color.RED, drawCircuit);
        drawCircuit.getRectangles().add(block);

        assertTrue(drawCircuit.isIntersecting(r2));
    }

    // Logic test: No intersection
    @Test
    void testRectangleNoIntersection()
    {
        Rectangle r1 = new Rectangle(50, 50, 50, 50);
        Rectangle r2 = new Rectangle(200, 200, 50, 50);

        Block block = new Moore("A", r1, Color.RED, drawCircuit);
        drawCircuit.getRectangles().add(block);

        assertFalse(drawCircuit.isIntersecting(r2));
    }

    @Test
    void testLineIntersectsRectangle()
    {
        Rectangle rect = new Rectangle(50, 50, 100, 100);
        Rectangle rect2 = new Rectangle(70, 70, 10, 10);
        Block block = new Moore("A", rect, Color.RED, drawCircuit);
        Block block2 = new Moore("A", rect2, Color.RED, drawCircuit);
        drawCircuit.getRectangles().add(block);
        drawCircuit.getRectangles().add(block2);

        //line is intersecting if it intersects with 2 rectangle objects
        Line2D line = new Line2D.Double(50, 50, 70, 70);

        assertTrue(drawCircuit.isIntersecting(line));
    }

    @Test
    void testLineContainedInRectangle()
    {
        Rectangle rect = new Rectangle(50, 50, 100, 100);
        Block block = new Moore("A", rect, Color.RED, drawCircuit);
        drawCircuit.getRectangles().add(block);

        //line is intersecting if it is contained inside a rectangle
        Line2D line = new Line2D.Double(50, 50, 60, 60);

        assertTrue(drawCircuit.isIntersecting(line));
    }

    @Test
    void testLineNotIntersectingRectangle()
    {
        Rectangle rect = new Rectangle(50, 50, 100, 100);
        Block block = new Moore("A", rect, Color.RED, drawCircuit);
        drawCircuit.getRectangles().add(block);

        //line is intersecting if it is contained inside a rectangle
        Line2D line = new Line2D.Double(50, 50, 180, 180);

        assertFalse(drawCircuit.isIntersecting(line));
    }

    @Test
    void testDeleteBlockRemovesRectangle()
    {
        Rectangle rect = new Rectangle(50, 50, 100, 100);
        Block block = new Moore("A", rect, Color.RED, drawCircuit);

        drawCircuit.getRectangles().add(block);
        assertEquals(1, drawCircuit.getRectangles().size());

        drawCircuit.deleteBlock(block);

        assertEquals(0, drawCircuit.getRectangles().size());
        assertFalse(drawCircuit.isIntersecting(rect));
    }

    @Test
    void testClearResetsAllState()
    {
        Rectangle rect = new Rectangle(50, 50, 100, 100);
        Block block = new Moore("A", rect, Color.RED, drawCircuit);
        drawCircuit.getRectangles().add(block);

        drawCircuit.clear();

        assertTrue(drawCircuit.getRectangles().isEmpty());
        assertTrue(drawCircuit.getWires().isEmpty());
    }

    @Test
    void testZoomChangesPreferredSize()
    {
        Dimension before = drawCircuit.getPreferredSize();

        drawCircuit.setZoom(2.0);

        Dimension after = drawCircuit.getPreferredSize();

        assertTrue(after.width > before.width);
        assertTrue(after.height > before.height);
    }
}
