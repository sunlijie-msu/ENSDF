/**
 * Command-line interface for ENSDF Averaging Tool
 * Uses the averagingAlgorithms package from AverageTool_22January2025.jar
 * 
 * Usage: java -cp "AverageTool_22January2025.jar;." AverageCLI "value1 unc1" "value2 unc2" ...
 * Example: java -cp "AverageTool_22January2025.jar;." AverageCLI "280 50" "215 70" "130 60" "120 65"
 */

import averagingAlgorithms.*;
import ensdf_datapoint.dataPt;

public class AverageCLI {
    
    public static void main(String[] args) {
        if (args.length == 0) {
            printUsage();
            return;
        }
        
        // Parse command-line arguments into dataPt array
        dataPt[] dataset = new dataPt[args.length];
        
        System.out.println("=".repeat(60));
        System.out.println("ENSDF AVERAGING TOOL - Command Line Interface");
        System.out.println("=".repeat(60));
        System.out.println();
        System.out.println("Input Data Points:");
        
        for (int i = 0; i < args.length; i++) {
            String[] parts = args[i].trim().split("\\s+");
            if (parts.length < 2) {
                System.err.println("Error: Each argument must be 'value uncertainty'");
                System.err.println("  Got: " + args[i]);
                return;
            }
            double value = Double.parseDouble(parts[0]);
            double unc = Double.parseDouble(parts[1]);
            dataset[i] = new dataPt(value, unc, unc, "Point " + (i+1));
            System.out.printf("  %d. %.1f ± %.1f%n", i+1, value, unc);
        }
        
        System.out.println();
        
        // Calculate weighted average
        averagingReport wtRpt = new averagingReport();
        dataPt weightedMean = averagingMethods.weightedAverage(dataset, wtRpt);
        
        // Calculate unweighted average
        averagingReport uwtRpt = new averagingReport();
        dataPt unweightedMean = averagingMethods.unweightedAverage(dataset, uwtRpt);
        
        // Get chi-squared values
        int n = dataset.length;
        double redChiSq = wtRpt.reducedChiSq;
        double critChiSq = averagingMethods.criticalChiSq(n - 1, 0.95, true);
        
        System.out.println("WEIGHTED AVERAGE:");
        System.out.printf("  Value: %.3f%n", weightedMean.getValue());
        System.out.printf("  Internal Uncertainty: %.3f%n", wtRpt.means[0].getLower());
        System.out.printf("  External Uncertainty: %.3f%n", wtRpt.means[1].getLower());
        System.out.println();
        
        System.out.println("UNWEIGHTED AVERAGE:");
        System.out.printf("  Value: %.3f%n", unweightedMean.getValue());
        System.out.printf("  Uncertainty: %.3f%n", unweightedMean.getLower());
        System.out.println();
        
        System.out.println("CHI-SQUARED TEST:");
        System.out.printf("  Chi^2/(N-1) = %.3f%n", redChiSq);
        System.out.printf("  Critical Chi^2/(N-1) at 95%% = %.3f%n", critChiSq);
        System.out.println();
        
        // Determine which average to use
        String recommendation;
        dataPt suggestedResult;
        if (redChiSq < critChiSq) {
            recommendation = "WEIGHTED (data are consistent)";
            suggestedResult = weightedMean;
        } else {
            recommendation = "UNWEIGHTED (data are inconsistent)";
            suggestedResult = unweightedMean;
        }
        
        System.out.println("RECOMMENDATION: Use " + recommendation);
        System.out.println();
        
        // Apply the minimum uncertainty rule
        double minUnc = Double.MAX_VALUE;
        for (dataPt pt : dataset) {
            minUnc = Math.min(minUnc, pt.getLower());
        }
        
        double finalValue = suggestedResult.getValue();
        double finalUnc = Math.max(suggestedResult.getLower(), minUnc);
        
        System.out.println("FINAL RESULT (with min uncertainty rule):");
        System.out.printf("  Minimum input uncertainty: %.3f%n", minUnc);
        System.out.printf("  Suggested Adopted Result: %.1f ± %.0f%n", finalValue, finalUnc);
        System.out.println();
        System.out.println("=".repeat(60));
    }
    
    private static void printUsage() {
        System.out.println("ENSDF Averaging Tool - Command Line Interface");
        System.out.println();
        System.out.println("Usage:");
        System.out.println("  java -cp \"AverageTool_22January2025.jar;.\" AverageCLI \"value1 unc1\" \"value2 unc2\" ...");
        System.out.println();
        System.out.println("Example:");
        System.out.println("  java -cp \"AverageTool_22January2025.jar;.\" AverageCLI \"280 50\" \"215 70\" \"130 60\" \"120 65\"");
        System.out.println();
        System.out.println("Each argument should be a quoted string with 'value uncertainty'");
    }
}
