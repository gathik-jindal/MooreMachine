/**
 * This is the DrawCircuit file which allows the user to draw different components on the panel. 
 * 
 * @author Aryan, Abhirath, Gathik
 * @version 1.0
 * @since 06/08/2024
 */

import java.awt.BasicStroke;
import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Component;
import java.awt.Cursor;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.FontMetrics;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import java.awt.Point;
import java.awt.Polygon;
import java.awt.Rectangle;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.awt.event.MouseWheelEvent;
import java.awt.event.MouseWheelListener;

import java.awt.geom.AffineTransform;
import java.awt.geom.Line2D;
import java.awt.geom.Point2D;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.Map;

import javax.swing.BorderFactory;
import javax.swing.JButton;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTextArea;
import javax.swing.SwingUtilities;

/**
 * Draw in which the user can draw the blocks.
 */
public class DrawCircuit extends JPanel 
{
    /**
     * Enum which determines whether the user wants to draw a box or a line.
     */
    public enum Mode {NONE, BOX, LINE}

    public static final double TOLERANCE = 10.0;    //Tolerance to determine whether the point is near
    private double zoom, translateX, translateY;    //Allows for zooming in and out
    private int baseWidth, baseHeight;              //The initial widths and heights of the panel
    private Mode drawingMode;                       //The initial drawing mode is None
    private Point startPoint;                       //The starting point for the box or line
    private ArrayList<Block> rectangles;            //An ArrayList object that contains all the rectangles
    private ArrayList<Block> wires;                 //An ArrayList object that contains all the wires
    private Rectangle currentRect;                  //The current rectangle being drawn
    private Line2D.Double currentLine;              //The current line being drawn
    private Color currentColor;                     //The current color of the object being drawm
    private Manager.Blocks currentName;             //The type of object being drawn
    private Manager manager;                        //The manager class
    private boolean isDragging;                     //Whether or not the user is dragging the mouse
    private Block highlightedBlock;                 //The highlight block (the selected block)

    /**
     * Creates a new DrawCircuit
     * @param manager : the Manager object in which this drawing panel is in
     */
    public DrawCircuit(Manager manager) 
    {
        setBackground(Color.WHITE);
        
        this.manager = manager;
        zoom = 1.0;
        drawingMode = Mode.NONE;
        rectangles = new ArrayList<>();
        wires = new ArrayList<>();
        isDragging = false;
        
        MouseAdapter mouseAdapter = new MouseAdapter() 
        {
            /**
             * Is called when the mouse is pressed
             * @param e : the mouse event
             */
            @Override
            public void mousePressed(MouseEvent e) 
            {
                if (SwingUtilities.isRightMouseButton(e)) 
                {
                    int x = (int)((e.getX() - translateX) / zoom);
                    int y = (int)((e.getY() - translateY) / zoom);
                    Point pt = new Point(x, y);
                    handleRightClick(pt);
                    repaint();
                } 
                else if (drawingMode == Mode.BOX) 
                {
                    int x = (int)((e.getX() - translateX) / zoom);
                    int y = (int)((e.getY() - translateY) / zoom);
                    startPoint = new Point(x, y);
                    currentRect = new Rectangle(startPoint);
                    adjustPreferredSize(currentRect);
                    repaint();
                }
                else if(drawingMode == Mode.LINE)
                {
                    int x = (int)((e.getX() - translateX) / zoom);
                    int y = (int)((e.getY() - translateY) / zoom);
                    startPoint = new Point(x, y);
                    currentLine = new Line2D.Double(startPoint, startPoint);
                    adjustPreferredSize(currentLine);
                    repaint();
                }
            }

            /**
             * Is called when the mouse is dragged.
             * @param e : the mouse event
             */
            @Override
            public void mouseDragged(MouseEvent e) 
            {
                if (drawingMode == Mode.BOX && startPoint != null) 
                {
                    isDragging = true;
                    int x = (int)((e.getX() - translateX) / zoom);
                    int y = (int)((e.getY() - translateY) / zoom);
                    Point pt = new Point(x, y);
                    updateRectangle(pt);
                    repaint();
                }
                else if(drawingMode == Mode.LINE && startPoint != null)
                {
                    isDragging = true;
                    int x = (int)((e.getX() - translateX) / zoom);
                    int y = (int)((e.getY() - translateY) / zoom);
                    Point pt = new Point(x, y);
                    updateLine(pt);
                    repaint();
                }
            }

            /**
             * Is called when the mouse is released.
             * @param e : the mouse event
             */
            @Override
            public void mouseReleased(MouseEvent e) 
            {
                if (drawingMode == Mode.BOX && startPoint != null) 
                {
                    if(isDragging)
                    {
                        int x = (int)((e.getX() - translateX) / zoom);
                        int y = (int)((e.getY() - translateY) / zoom);
                        Point pt = new Point(x, y);
                        updateRectangle(pt);
                        isDragging = false;

                        if(!isIntersecting(currentRect))    
                        {
                            rectangles.add(manager.createBlock(currentName, null, currentRect, currentColor));
                            handleRightClick(new Point(currentRect.x + currentRect.width/2, currentRect.y + currentRect.height/2));
                        }
                    }

                    repaint();
                    startPoint = null;
                    currentRect = null;            
                }
                else if(drawingMode == Mode.LINE && startPoint != null)
                {
                    if(isDragging)
                    {
                        int x = (int)((e.getX() - translateX) / zoom);
                        int y = (int)((e.getY() - translateY) / zoom);
                        Point pt = new Point(x, y);
                        updateLine(pt);
                        isDragging = false;

                        if(!isIntersecting(currentLine))
                        {
                            wires.add(manager.createBlock(currentName, currentLine, null, currentColor));
                            handleRightClick(wires.getLast());
                        }
                    }

                    repaint();
                    startPoint = null;
                    currentLine = null;
                }
            }
        };

        addMouseWheelListener(new MouseWheelListener() 
        {
            /**
             * Is called when the mouse wheel moves.
             * 
             * @param e : the mouse wheel event
             */
            @Override
            public void mouseWheelMoved(MouseWheelEvent e) 
            {
                double oldZoom = zoom;
                if (e.getPreciseWheelRotation() < 0) 
                {
                    manager.setZoomValue(5);
                } 
                else 
                {
                    manager.setZoomValue(-5);
                }
                double newZoom = manager.getZoomValue() / 100.0;
                setZoom(newZoom, e.getX(), e.getY(), oldZoom);
                revalidate();
                repaint();
            }
        });

        addMouseListener(mouseAdapter);
        addMouseMotionListener(mouseAdapter);
    }

    /**
     * Sets the zoom value to the one given.
     * @param zoom : the new zoom value
    */
    public void setZoom(double zoom)
    {
        this.zoom = zoom;
        revalidate();
        repaint();
    }

    /**
     * Sets the zoom value to the one given taking into considerations the previous zoom value.
     * @param newZoom : the new zoom value
     * @param x : the old translateX coordinate
     * @param y : the old translateY coordinate
     * @param oldZoom : the old zoom value
     */
    private void setZoom(double newZoom, int x, int y, double oldZoom)
    {
        double oldZoomX = (x - translateX) / oldZoom;
        double oldZoomY = (y - translateY) / oldZoom;
        translateX = x - oldZoomX * newZoom;
        translateY = y - oldZoomY * newZoom;
        setZoom(newZoom);
    }

    /**
     * Resets the variables.
     */
    private void reset()
    {
        isDragging = false;
        highlightedBlock = null;
        manager.getInfoPanel().removeInfo();
        repaint();
    }

    /**
     * Is called to handle right clicked events.
     * @param point : the point where the mouse is clicked
     */
    private void handleRightClick(Point point) 
    {
        for(Block block : rectangles) 
        {
            if(block.getRect().contains(point)) 
            {
                handleRightClick(block);
                return;
            }
        }

        for (Block wire : wires) 
        {
            if (isPointNearLine(wire.getLine(), point, TOLERANCE)) 
            {
                handleRightClick(wire);
                return;
            }
        }
    }

    /**
     * Is called to handle the clicked events.
     * @param block : the block which is closest to the point where the mouse clicked.
     */
    private void handleRightClick(Block block)
    {
        manager.getInfoPanel().updateInfo(block.getMap());
        highlightedBlock = block;
    }
    
    /**
     * @param line : the line to check if the point is near
     * @param point : the point to check if the line is near
     * @param tolerance : the tolerance level
     * @return true if the point is close to the line within tolerance level; false otherwise
     */
    private boolean isPointNearLine(Line2D line, Point point, double tolerance) 
    {
        double dx = line.getX2() - line.getX1();
        double dy = line.getY2() - line.getY1();
        double length = Math.sqrt(dx * dx + dy * dy);

        double ux = dx / length;
        double uy = dy / length;

        double px = -uy;
        double py = ux;

        Point2D.Double p1 = new Point2D.Double(line.getX1() + px * tolerance, line.getY1() + py * tolerance);
        Point2D.Double p2 = new Point2D.Double(line.getX1() - px * tolerance, line.getY1() - py * tolerance);
        Point2D.Double p3 = new Point2D.Double(line.getX2() + px * tolerance, line.getY2() + py * tolerance);
        Point2D.Double p4 = new Point2D.Double(line.getX2() - px * tolerance, line.getY2() - py * tolerance);

        Polygon bufferPolygon = new Polygon();
        bufferPolygon.addPoint((int) p1.x, (int) p1.y);
        bufferPolygon.addPoint((int) p3.x, (int) p3.y);
        bufferPolygon.addPoint((int) p4.x, (int) p4.y);
        bufferPolygon.addPoint((int) p2.x, (int) p2.y);

        return bufferPolygon.contains(point);

    }

    /**
     * Sets the drawing mode.
     * @param mode : the drawing mode
     * @param color : the current color
     * @param name : the type of object
     */
    public void setDrawingMode(Mode mode, Color color, Manager.Blocks name) 
    {
        this.drawingMode = mode;
        this.currentColor = color;
        this.currentName = name;
    }

    /**
     * Updates the current rectangle.
     * @param endPoint : the other end point of the rectangle
     */
    private void updateRectangle(Point endPoint) 
    {
        int x = Math.min(startPoint.x, endPoint.x);
        int y = Math.min(startPoint.y, endPoint.y);
        int width = Math.abs(startPoint.x - endPoint.x);
        int height = Math.abs(startPoint.y - endPoint.y);
        currentRect.setBounds(x, y, width, height);
        adjustPreferredSize(currentRect);
    }

    /**
     * Updates the current line
     * @param endPoint : the other end point of the line
     */
    private void updateLine(Point endPoint)
    {
        currentLine.setLine(startPoint, endPoint);
        adjustPreferredSize(currentLine);
    }

    /**
     * Paints the drawing panel.
     * @param g : the Graphics object
     */
    @Override
    protected void paintComponent(Graphics g) 
    {
        super.paintComponent(g);

        manager.setClosestBlock(false);

        Graphics2D g2 = (Graphics2D) g;
        g2.translate(translateX, translateY);
        g2.scale(zoom, zoom);

        g2.setStroke(new BasicStroke(4));

        g.setFont(new Font("Arial", Font.BOLD, 15));
        g.setColor(Color.BLACK);
        
        //paints all the blocks
        for (Block block : rectangles) 
        {
            Rectangle rect = block.getRect();
            
            g.setColor(block.getColor());

            g.fillRect(rect.x, rect.y, rect.width, rect.height);

            //is the block the selected block
            if(block == highlightedBlock)
                g.setColor(Color.MAGENTA);
            else
                g.setColor(Color.black);

            g2.drawRect(rect.x, rect.y, rect.width, rect.height);
            FontMetrics metrics = g.getFontMetrics();
            int textWidth = metrics.stringWidth(block.getName());
            int textHeight = metrics.getHeight();
            int textX = rect.x + (rect.width - textWidth) / 2;
            int textY = rect.y + (rect.height - textHeight) / 2 + metrics.getAscent();

            //if the user wants to plot the block, then the text color should be black
            if(block.getPlot().equals("True"))
                g.setColor(Color.BLACK);
            else
                g.setColor(Color.WHITE);

            g.drawString(block.getName(), textX, textY);
        }

        //paints all the wires
        for (Block block : wires)
        {
            ((Wire)(block)).updateBlocks();
            Line2D.Double line = block.getLine();
            
            g.setColor(block.getColor());

            if(block == highlightedBlock)
                g.setColor(Color.MAGENTA);
            else if(((Wire)(block)).isClocked())
                g.setColor(new Color(255, 127, 80));

            int x1 = (int)(line.x1), y1 = (int)(line.y1), x2 = (int)(line.x2), y2 = (int)(line.y2);
    
            g.drawLine(x1, y1, x2, y2);
            
            g.fillOval(x1 - 5, y1 - 5, 10, 10);
            
            double angle = Math.atan2(y2 - y1, x2 - x1);
            
            g.drawPolygon(((Wire)(block)).getArrowHead());

            //Draws the bits of the wires
            String startText = ((Wire)(block)).getOutputString();
            FontMetrics metrics = g.getFontMetrics(g.getFont());

            AffineTransform originalTransform = g2.getTransform();
            
            int startTextX = x1 - metrics.stringWidth(startText) / 2;
            int startTextY = y1 - 10;
            g2.rotate(angle, x1, y1);
            g2.drawString(startText, startTextX, startTextY);
            
            g2.setTransform(originalTransform);
        }

        if (currentRect != null) 
        {
            g.setColor(currentColor);
            g.fillRect(currentRect.x, currentRect.y, currentRect.width, currentRect.height);
            g.setColor(Color.black);
            g2.drawRect(currentRect.x, currentRect.y, currentRect.width, currentRect.height);
        }

        if(currentLine != null)
        {
            g.setColor(currentColor);
            g.drawLine((int)(currentLine.x1), (int)(currentLine.y1), (int)(currentLine.x2), (int)(currentLine.y2));
        }
    }

    /**
     * @param r1 : the rectangle to check
     * @return true if this rectangle intersects with any object; false otherwise
     */
    public boolean isIntersecting(Rectangle r1) 
    {
        for(Block block:rectangles)
        {
            if(block.getRect().intersects(r1))
                return true;
        }

        for(Block block:wires)
        {
            if(r1.intersectsLine(block.getLine()) && (!isTouchingBorder(r1, block.getLine()) || r1.contains(block.getLine().getP1()) || r1.contains(block.getLine().getP2())))
                return true;
        }

        return false;
    }

    /**
     * @param l1 : the line to check
     * @return true if this line intersects any object; false otherwise
     */
    public boolean isIntersecting(Line2D l1) 
    {
        int intersectingRectanglesCount = 0;
        
        for (Block block : rectangles) 
        {
            Rectangle rect = block.getRect();
            
            if (rect.contains(l1.getP1()) && rect.contains(l1.getP2())) 
            {
                return true;
            }
            
            if (rect.intersectsLine(l1)) 
            {
                intersectingRectanglesCount++;
                if (intersectingRectanglesCount > 2) 
                {
                    return true;
                }
            }
        }

        for (Block block : rectangles) 
        {
            Rectangle rect = block.getRect();
            if (rect.contains(l1.getP1())) 
            {
                l1.setLine(shortenLineStart(l1, rect).getP1(), l1.getP2());
                if (!rect.intersectsLine(l1)) break;
            }
        }

        for (Block block : rectangles) 
        {
            Rectangle rect = block.getRect();
            if (rect.contains(l1.getP2())) 
            {
                l1.setLine(l1.getP1(), shortenLineEnd(l1, rect).getP2());
                if (!rect.intersectsLine(l1)) break;
            }
        }

        for (Block block : wires) 
        {
            if (l1.intersectsLine(block.getLine())) 
            {
                return true;
            }
        }

        return false;
    }

    /**
     * Shortens the line's starting point until it no longer intersects the rectangle
     * @param l1 : the line to shorten
     * @param rect : the rectangle that this line intersects
     * @return a new line which does not intersect the rectangle
     */
    private static Line2D shortenLineStart(Line2D l1, Rectangle rect) 
    {
        double dx = l1.getX2() - l1.getX1();
        double dy = l1.getY2() - l1.getY1();
        double step = Math.min(Math.abs(dx), Math.abs(dy)) * 0.1;
        
        while (rect.contains(l1.getP1())) 
        {
            l1.setLine(l1.getX1() + step, l1.getY1() + step, l1.getX2(), l1.getY2());
        }
        
        return l1;
    }

    /**
     * Shortens the line's ending point until it no longer intersects the rectangle
     * @param l1 : the line to shorten
     * @param rect : the rectangle that this line intersects
     * @return a new line which does not intersect the rectangle
     */
    private static Line2D shortenLineEnd(Line2D l1, Rectangle rect) 
    {
        double dx = l1.getX2() - l1.getX1();
        double dy = l1.getY2() - l1.getY1();
        double step = Math.min(Math.abs(dx), Math.abs(dy)) * 0.1;
        
        while (rect.contains(l1.getP2())) 
        {
            l1.setLine(l1.getX1(), l1.getY1(), l1.getX2() - step, l1.getY2() - step);
        }
        
        return l1;
    }
    
    /**
     * @param rect : the rectangle
     * @param line : the line
     * @return true if the rectangle touches the border of the line
     */
    private boolean isTouchingBorder(Rectangle rect, Line2D line) 
    {
        Line2D top = new Line2D.Double(rect.getMinX(), rect.getMinY(), rect.getMaxX(), rect.getMinY());
        Line2D bottom = new Line2D.Double(rect.getMinX(), rect.getMaxY(), rect.getMaxX(), rect.getMaxY());
        Line2D left = new Line2D.Double(rect.getMinX(), rect.getMinY(), rect.getMinX(), rect.getMaxY());
        Line2D right = new Line2D.Double(rect.getMaxX(), rect.getMinY(), rect.getMaxX(), rect.getMaxY());
    
        return top.intersectsLine(line) || bottom.intersectsLine(line) || left.intersectsLine(line) || right.intersectsLine(line);
    }

    /**
     * @return an ArrayList object that contains all the rectangles
     */
    public ArrayList<Block> getRectangles()
    {
        return rectangles;
    }

    /**
     * @return an ArrayList object that contains all the wires
     */
    public ArrayList<Block> getWires()
    {
        return wires;
    }

    /**
     * Deletes the block from the block list
     * @param block : the block to remove
     */
    public void deleteBlock(Block block)
    {
        for(Block b : rectangles)
        {
            if(b == block)
            {
                rectangles.remove(b);
                reset();
                return;
            }
        }

        for(Block b : wires)
        {
            if(b == block)
            {
                wires.remove(b);
                reset();
                return;
            }
        }
    }

    /**
     * Resets everything
     */
    public void clear()
    {
        Block.reset();
        zoom = 1.0;
        translateX = translateY = 0;
        drawingMode = Mode.NONE;
        startPoint = null;
        rectangles.clear();
        wires.clear();
        currentRect = null;
        currentColor = null;
        currentName = null;
        isDragging = false;
        highlightedBlock = null;
        manager.getInfoPanel().removeInfo();
        manager.getInfoPanel().getTextArea().setText("");
        setCursor(Cursor.getPredefinedCursor(Cursor.DEFAULT_CURSOR));
    }   

    /**
     * Used to change the width and height of the panel
     */
    @Override
    public void addNotify()
    {
        super.addNotify();
        baseWidth = getWidth();
        baseHeight = getHeight();
    }

    /**
     * Adjusts the preferred size of the window after a rectangle is drawn
     * @param rect : the drawn rectangle
     */
    private void adjustPreferredSize(Rectangle rect)
    {
        int x1 = rect.x, y1 = rect.y, x2 = rect.x + rect.width, y2 = rect.y + rect.height;
        adjustPreferredSize(x1, y1, x2, y2);
    }

    /**
     * Adjusts the preferred size of the window after a line is drawn
     * @param line : the drawn line
     */
    private void adjustPreferredSize(Line2D line)
    {
        int x1 = (int)(line.getX1()), y1 = (int)(line.getY1()), x2 = (int)(line.getX2()), y2 = (int)(line.getY2());
        adjustPreferredSize(x1, y1, x2, y2);
    }

    /**
     * Adjusts the preferred size of the window after somethign is drawn
     * @param x1 : x1 coordinate
     * @param y1 : y1 coordinate
     * @param x2 : x2 coordinate
     * @param y2 : y2 coordinate
     */
    private void adjustPreferredSize(int x1, int y1, int x2, int y2)
    {
        int maxX = (int) (Math.max(x1, x2) / zoom);
        int maxY = (int) (Math.max(y1, y2) / zoom);
        baseWidth = Math.max(baseWidth, maxX + 50);
        baseHeight = Math.max(baseHeight, maxY + 50);
        setPreferredSize(new Dimension(baseWidth, baseHeight));
        revalidate();
    }

    /**
     * @return Dimension: the preferred size of this panel
     */
    @Override
    public Dimension getPreferredSize() 
    {
        if (baseWidth == 0 || baseHeight == 0) 
        {
            baseWidth = getWidth();
            baseHeight = getHeight();
        }

        int width = (int) (baseWidth * zoom);
        int height = (int) (baseHeight * zoom);
            
        return new Dimension(width, height);
    }
}

/**
 * This class handles the information of each Block
 */
class InfoPanel extends JPanel 
{
    private Map<String, Component> infoMap; //this map contains the information where the first element is the header and Component is the component to be drawn
    private JPanel infoPanel;               //this panel is the main center panel that contains the information
    private JTextArea textArea;             //this textArea is used for writing the functions

    /**
     * Creates a new information panel
     * @param manage : the manager class
     */
    public InfoPanel(Manager manage)    
    {
        this.setLayout(new BorderLayout());
        this.setPreferredSize(new Dimension(350, 0));

        //Header label at the top
        JLabel headerLabel = new JLabel("Right click on block or wire to get information about it");
        headerLabel.setFont(new Font("Arial", Font.BOLD, 13));
        headerLabel.setForeground(Color.BLUE);
        headerLabel.setHorizontalAlignment(JLabel.CENTER);
        headerLabel.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));

        this.add(headerLabel, BorderLayout.NORTH);

        //infoPanel containing the information in the center
        infoPanel = new JPanel();
        infoPanel.setLayout(new GridBagLayout());
        infoPanel.setBackground(Color.YELLOW);
        infoPanel.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));

        this.add(infoPanel, BorderLayout.CENTER);

        //southPanel containing the generate button and the textArea
        JPanel southPanel = new JPanel(new BorderLayout());

        JButton generateFile = new JButton("Generate Code");
        generateFile.setFont(new Font("Arial", Font.BOLD, 13));
        generateFile.setBackground(new Color(173, 216, 230));
        generateFile.setHorizontalAlignment(JButton.CENTER);
        generateFile.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));
        
        //change the color of the button when the mouse is hovering
        generateFile.addMouseListener(new MouseAdapter() 
        {
            /**
             * Is called when the mouse enters the button.
             * @param evt : the mouse event
             */
            @Override
            public void mouseEntered(MouseEvent evt) 
            {
                generateFile.setBackground(Color.CYAN);
            }

            /**
             * Is called when the mouse exits the button.
             * @param evt : the mouse event
             */
            @Override
            public void mouseExited(MouseEvent evt) 
            {
                generateFile.setBackground(new Color(173, 216, 230));
            }
        });

        //creates the python file when the button is clicked
        generateFile.addActionListener(new ActionListener() 
        {
            /**
             * Is called when the button is clicked.
             * @param e : the action event
             */
            @Override
            public void actionPerformed(ActionEvent e) 
            {
                if(manage.setClosestBlock(true))
                    if(manage.isValidConnections(manage.getDrawCircuit().getWires()))
                    {
                        manage.generateFile(getTextArea());
                    }
            } 
        });

        southPanel.add(generateFile, BorderLayout.SOUTH);

        //center panel for the south panel where the user can write functions
        JPanel centerPanel = new JPanel(new BorderLayout());

        JLabel functions = new JLabel(manage.getFunctionLabel());
        functions.setFont(new Font("Arial", Font.BOLD, 13));
        functions.setForeground(Color.BLUE);
        functions.setHorizontalAlignment(JLabel.CENTER);
        functions.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));

        textArea = new JTextArea("");
        textArea.setLineWrap(true);
        textArea.setWrapStyleWord(true);
        textArea.setTabSize(4);

        JScrollPane scrollPane = new JScrollPane(textArea);
        scrollPane.setPreferredSize(new Dimension(200, 200));

        centerPanel.add(functions, BorderLayout.NORTH);
        centerPanel.add(scrollPane, BorderLayout.CENTER);

        southPanel.add(centerPanel, BorderLayout.CENTER);

        this.add(southPanel, BorderLayout.SOUTH);

        infoMap = new LinkedHashMap<>();
    }

    /**
     * Clears the center panel and removes all information.
     */
    public void removeInfo()
    {
        infoPanel.removeAll();
        this.revalidate();
        this.repaint();
    }

    /**
     * Sets the information objects to the one given
     * @param info : a map containing the label and the component
     */
    public void updateInfo(Map<String, Component> info) 
    {
        removeInfo();

        for (String label : info.keySet()) 
        {
            JLabel jLabel = new JLabel(label);
            jLabel.setFont(new Font("Arial", Font.BOLD, 12));
            jLabel.setForeground(Color.DARK_GRAY);
            jLabel.setHorizontalAlignment(JLabel.CENTER);

            GridBagConstraints gbc = new GridBagConstraints();
            gbc.fill = GridBagConstraints.HORIZONTAL;
            gbc.weightx = 1.0;
            gbc.gridx = 0;
            gbc.gridy = GridBagConstraints.RELATIVE;
            gbc.anchor = GridBagConstraints.CENTER;

            Component comp = info.get(label);
            infoMap.put(label, comp);

            infoPanel.add(jLabel, gbc);

            gbc.gridy = GridBagConstraints.RELATIVE;
            infoPanel.add(javax.swing.Box.createVerticalStrut(5), gbc);

            gbc.gridy = GridBagConstraints.RELATIVE;
            infoPanel.add(comp, gbc);

            gbc.gridy = GridBagConstraints.RELATIVE;
            infoPanel.add(javax.swing.Box.createVerticalStrut(10), gbc);
        }

        this.revalidate();
        this.repaint();
    }

    /**
     * @return textArea : the functions text area
     */
    public JTextArea getTextArea()
    {
        return this.textArea;
    }
}