/**
 * This is the manager class that holds all the JPanels. 
 * 
 * @author Aryan, Abhirath, Gathik
 * @version 1.0
 * @since 06/08/2024
 */

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Point;
import java.awt.Rectangle;
import java.awt.geom.Line2D;
import java.util.ArrayList;

import javax.swing.JFrame;
import javax.swing.JOptionPane;
import javax.swing.JPanel;

public class Manager extends JPanel 
{
    private MenuBar bar;                //The MenuBar that goes at the top of the Panel
    private DrawingPanel drawingPanel;  //The drawing panel that goes in the center of the Panel
    private InfoPanel infoPanel;        //The information panel that allows the user to look at information regarding the blocks 
    private JFrame frame;               //The frame object.

    /**
     * The blocks enum which stores the name of the blocks.
     */
    public enum Blocks
    {
        INPUT("Input Block"), MOORE("Moore Machine"), COMB("Combinational Block"), 
        OUTPUT("Output Block"), CLOCK("Clock"), WIRE("Wire");

        private String name;            //The name of the block

        /**
         * Sets the name of the block
         * @param name : the name of the block
         */
        private Blocks(String name)
        {
            this.name = name;
        }

        /**
         * @return the name of the block
         */
        public String getName()
        {
            return name;
        }
    }

    /**
     * Creates a manager object.
     * @param frame : the frame in which this panel would be placed in
     */
    public Manager(JFrame frame) 
    {
        super(new BorderLayout());
        
        bar = new MenuBar(this);
        this.add(bar, BorderLayout.NORTH);

        drawingPanel = new DrawingPanel(this);
        this.add(drawingPanel, BorderLayout.CENTER);

        infoPanel = new InfoPanel(this);
        this.add(infoPanel, BorderLayout.WEST);

        this.frame = frame;
    }

    /**
     * @return the drawing panel object
     */
    public DrawingPanel getDrawingPanel() 
    {
        return drawingPanel;
    }

    /**
     * @return the info panel object
     */
    public InfoPanel getInfoPanel() 
    {
        return infoPanel;
    }

    /**
     * Creates a new block from the inputs specified.
     * If the block is a Wire, then a line is added. Otherwise, a rectangle is added.
     * @param block : The type of block you want
     * @param line : a line object to represent a wire
     * @param rect : a rectangle object to represent all other blocks
     * @param color : the color of this block
     * @return a new Block object
     */
    public Block createBlock(Blocks block, Line2D.Double line, Rectangle rect, Color color)
    {
        switch(block)
        {
            case INPUT:
                return new Input(block.getName(), rect, color, drawingPanel);
            case OUTPUT:
                return new Output(block.getName(), rect, color, drawingPanel);
            case MOORE:
                return new Moore(block.getName(), rect, color, drawingPanel);
            case CLOCK:
                return new Clock(block.getName(), rect, color, drawingPanel);
            case COMB:
                return new Combinational(block.getName(), rect, color, drawingPanel);
            case WIRE:
                return new Wire(block.getName(), line, color, drawingPanel);
            default:
                return null;
        }
    }

    /**
     * This method sets the closest block for all the wires, i.e., the starting and the ending blocks that the wire connects.
     * @param showMessageDialog : whether or not to show any error messages
     * @return true if all wires have been connected properly; false otherwise
     */
    public boolean setClosestBlock(boolean showMessageDialog) 
    {
        ArrayList<Block> wires = drawingPanel.getWires();
        ArrayList<Block> rectangles = drawingPanel.getRectangles();
    
        double thresholdDistance = 400.0;
    
        for (Block wire : wires) 
        {
            Point [] endPoints;
            Point arrowTip = new Point(((Wire)(wire)).getArrowHead().xpoints[0], ((Wire)(wire)).getArrowHead().ypoints[0]);

            endPoints = new Point []
            {
                new Point((int)(wire.getLine().x1), (int)(wire.getLine().y1)),
                arrowTip
            };

            for (int i = 0; i < endPoints.length; i++) 
            {
                Point endPoint = endPoints[i];
                boolean isStartPoint = (i == 0);
                double closestDistance = Double.MAX_VALUE;
                Block closestBlock = null;
                
                //Loop through all the rectangles and see which rectangle is closest
                for (Block rectangle : rectangles) 
                {
                    Rectangle rect = rectangle.getRect();
                    Point[] rectPoints = 
                    {
                        new Point(rect.x, rect.y),
                        new Point(rect.x + rect.width, rect.y),
                        new Point(rect.x, rect.y + rect.height),
                        new Point(rect.x + rect.width, rect.y + rect.height)
                    };
    
                    for (Point rectPoint : rectPoints) 
                    {
                        double distance = endPoint.distance(rectPoint);
                        if (distance < closestDistance) 
                        {
                            closestDistance = distance;
                            closestBlock = rectangle;
                        }
                    }
                }
                
                //Loops through all the wires and sees which wire is the closest
                for (Block otherWire : wires) 
                {
                    if (otherWire == wire) continue;
    
                    Point[] wirePoints = 
                    {
                        new Point((int)(otherWire.getLine().x1), (int)(otherWire.getLine().y1)),
                        new Point((int)(otherWire.getLine().x2), (int)(otherWire.getLine().y2))
                    };
    
                    for (int j = 0; j < wirePoints.length; j++) 
                    {
                        Point wirePoint = wirePoints[j];
                        boolean isOtherStartPoint = (j == 0);
                        
                        //only allow those wires to be "close" to each other who have their opposite ends close together
                        if ((isStartPoint && !isOtherStartPoint) || (!isStartPoint && isOtherStartPoint)) 
                        {
                            double distance = endPoint.distance(wirePoint);
                            if (distance < closestDistance) 
                            {
                                closestDistance = distance;
                                closestBlock = otherWire;
                            }
                        }
                    }
                }
                
                //if the closest distance to any block is greater than the threshold, the connections have not been done properly.
                //In this case we return false.
                if (closestDistance > thresholdDistance) 
                {
                    if(showMessageDialog)
                        JOptionPane.showMessageDialog(null, "Invalid Connections. Check wire connections.", "Error", JOptionPane.ERROR_MESSAGE);
                    return false;
                }
                
                ((Wire)(wire)).setBlock(closestBlock);
            }
        }
        
        //Find the closest rectangular block
        for (Block wire : wires) 
        {
            Block currentBlock = ((Wire)(wire)).getStartBlock();
            Wire currentWire = (Wire)(wire);
            boolean foundRectangle = !(currentBlock instanceof Wire);
            
            //Loop through the wire connections until you get to one wire which has starting connection to a rectangle.
            while (currentBlock instanceof Wire) 
            {
                Wire connection = (Wire) currentBlock;
                Block endBlock = connection.getStartBlock();
                currentWire = connection;
                if (endBlock instanceof RectangleBlock) 
                {
                    foundRectangle = true;
                    currentBlock = endBlock;
                    break;
                }
                else if(currentBlock == endBlock)
                {
                    if(showMessageDialog)
                        JOptionPane.showMessageDialog(null, "Invalid Connections. Check wire connections.", "Error", JOptionPane.ERROR_MESSAGE);
                    return false;
                } 
                else 
                {
                    currentBlock = endBlock;
                }
            }
    
            if (foundRectangle) 
            {
                Wire connection = (Wire) wire;
                connection.setStartBlock(currentBlock, currentWire);
            } 
            else 
            {
                if(showMessageDialog)
                    JOptionPane.showMessageDialog(null, "Invalid Connections. Check wire connections.", "Error", JOptionPane.ERROR_MESSAGE);
                return false;
            }
        }
    
        return true;
    }
    
    /**
     * Checks if all the wires are connected to valid rectangles.
     * It is advised to first check if all the wires are actually connected or not via the above method.
     * @param wires : An ArrayList of Block that contains all wires
     * @return true if all connections are valid; false otherwise
     * @see setClosestBlock
     */
    public boolean isValidConnections(ArrayList<Block> wires)
    {
        for(Block w : wires)
        {
            Wire wire = (Wire)(w);
            if(wire.getStartBlock() instanceof RectangleBlock && wire.getEndBlock() instanceof RectangleBlock)
            {
                RectangleBlock startBlock = (RectangleBlock)(wire.getStartBlock());
                RectangleBlock endBlock = (RectangleBlock)(wire.getEndBlock());
                
                //startBlock needs to have output connections and endBlock needs to have input connections
                if(startBlock.hasOutput() && endBlock.hasInput()) continue;
                else if(startBlock.hasOutput())
                {
                    wires.remove(w);
                    drawingPanel.repaint();
                    JOptionPane.showMessageDialog(null, "Invalid wire detected and deleted. " + 
                        "Note: " + endBlock.getType() + " has no input connections.", "Error.", JOptionPane.ERROR_MESSAGE);
                    return false;
                }
                else
                {
                    wires.remove(w);
                    drawingPanel.repaint();
                    JOptionPane.showMessageDialog(null, "Invalid wire detected and deleted. " + 
                        "Note: " + startBlock.getType() + " has no output connections.", "Error.", JOptionPane.ERROR_MESSAGE);
                    return false;
                }
            }
        }

        return true;
    }

    /**
     * @return the frame object that this class is part of
     */
    public JFrame getFrame()
    {
        return this.frame;
    }
}