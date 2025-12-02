/*      */ package averagingAlgorithms;
/*      */ 
/*      */ import ensdf_datapoint.dataPt;
/*      */ import java.util.ArrayList;
/*      */ import java.util.Arrays;
/*      */ import java.util.List;
/*      */ import java.util.function.DoubleFunction;
/*      */ import java.util.function.Function;
/*      */ import javax.swing.JOptionPane;
/*      */ 
/*      */ public final class averagingMethods {
/*   33 */   private static List<CriticalChiSquare> previousCritChiSq = null;
/*      */   
/*   34 */   private static int lastCritChiSqIndex = 0;
/*      */   
/*   40 */   public static double critChiSqConf = 0.95D;
/*      */   
/*      */   public static final dataPt unweightedAverage(dataPt[] dataset, averagingReport rpt) {
/*   58 */     int n = dataset.length;
/*   59 */     dataPt result = new dataPt(0.0D, 0.0D, 0.0D, "Unweighted Average");
/*      */     int i;
/*   60 */     for (i = 0; i < n; i++)
/*   61 */       result.addToValue(dataset[i].getValue()); 
/*   63 */     result.setValue(result.getValue() / n);
/*   65 */     double[] deviationArray = new double[n];
/*   66 */     double externaluncert = 0.0D;
/*   67 */     double internaluncert = 0.0D;
/*   68 */     for (i = 0; i < n; i++) {
/*   69 */       deviationArray[i] = Math.pow(result.getValue() - dataset[i].getValue(), 2.0D);
/*   70 */       externaluncert += deviationArray[i];
/*   71 */       internaluncert += dataset[i].gaussVariance();
/*      */     } 
/*   73 */     externaluncert = Math.sqrt(externaluncert / n * (n - 1));
/*   74 */     internaluncert = Math.sqrt(internaluncert) / n;
/*   75 */     result.setUpper(Math.max(internaluncert, externaluncert));
/*   76 */     result.setLower(result.getUpper());
/*      */     try {
/*   79 */       rpt.differenceFromMeanSq = (double[])deviationArray.clone();
/*   80 */       rpt.originalDataSet = dataset;
/*   81 */       rpt.means = new dataPt[1];
/*   82 */       rpt.means[0] = new dataPt(result);
/*   83 */       rpt.methodName = "Unweighted Average";
/*   84 */     } catch (NullPointerException nullPointerException) {}
/*   88 */     return result;
/*      */   }
/*      */   
/*      */   public static final dataPt unweightedAverage(dataPt[] dataset) {
/*   98 */     return unweightedAverage(dataset, null);
/*      */   }
/*      */   
/*      */   public static final double WeightedAveChiSq(dataPt[] dataset, double mean) {
/*  114 */     double result = 0.0D;
/*      */     byte b;
/*      */     int i;
/*      */     dataPt[] arrayOfDataPt;
/*  115 */     for (i = (arrayOfDataPt = dataset).length, b = 0; b < i; ) {
/*      */       double w;
/*  115 */       dataPt datapt = arrayOfDataPt[b];
/*  129 */       double dxm = datapt.getLower();
/*  130 */       double dxp = datapt.getUpper();
/*  131 */       if (dxp < 0.0D)
/*  131 */         dxp = 0.0D; 
/*  132 */       if (dxm < 0.0D)
/*  132 */         dxm = 0.0D; 
/*  134 */       double V = Math.pow(dxp + dxm, 2.0D) / 4.0D + 0.3633802276324186D * Math.pow(dxp - dxm, 2.0D) / 4.0D;
/*  135 */       if (V == 0.0D) {
/*  136 */         w = 0.0D;
/*      */       } else {
/*  138 */         w = 1.0D / V;
/*      */       } 
/*  140 */       result += w * Math.pow(datapt.getValue() - mean, 2.0D);
/*      */       b++;
/*      */     } 
/*  144 */     return result;
/*      */   }
/*      */   
/*      */   public static final dataPt weightedAverage_legacy(dataPt[] dataset, boolean forceInternalUncert, averagingReport rpt) {
/*  175 */     int n = dataset.length;
/*  176 */     double[] normWeight = new double[n];
/*  177 */     double weightSum = 0.0D;
/*  178 */     double lowerTot = 0.0D;
/*  179 */     double upperTot = 0.0D;
/*      */     int i;
/*  181 */     for (i = 0; i < n; i++) {
/*  182 */       normWeight[i] = 1.0D / dataset[i].gaussVariance();
/*  183 */       lowerTot += dataset[i].getLower() * dataset[i].getLower();
/*  184 */       upperTot += dataset[i].getUpper() * dataset[i].getUpper();
/*  185 */       weightSum += normWeight[i];
/*      */     } 
/*  188 */     dataPt result = new dataPt();
/*  189 */     result.setName("Weighted Average");
/*  190 */     result.setValue(0.0D);
/*  191 */     for (i = 0; i < n; i++) {
/*  192 */       normWeight[i] = normWeight[i] / weightSum;
/*  193 */       result.addToValue(normWeight[i] * dataset[i].getValue());
/*      */     } 
/*  196 */     result.setLower(Math.sqrt(2.0D / (1.0D + upperTot / lowerTot) / weightSum));
/*  198 */     result.setUpper(Math.sqrt(2.0D / (1.0D + lowerTot / upperTot) / weightSum));
/*  200 */     double symIntUnc = Math.sqrt(1.0D / weightSum);
/*  203 */     if (Math.abs(result.getLower() / result.getUpper() - 1.0D) < 0.01D) {
/*  204 */       result.setLower(symIntUnc);
/*  205 */       result.setUpper(symIntUnc);
/*      */     } 
/*  208 */     double chiSq = WeightedAveChiSq(dataset, result.getValue());
/*  209 */     double extUnc = Math.sqrt(chiSq / weightSum * (n - 1));
/*      */     try {
/*  212 */       rpt.originalDataSet = dataset;
/*  213 */       rpt.means = new dataPt[2];
/*  214 */       rpt.means[0] = new dataPt(result);
/*  215 */       rpt.means[0].setName("Weighted Average (Internal Uncertainty)");
/*  216 */       rpt.means[1] = new dataPt(result.getValue(), extUnc, extUnc, 
/*  217 */           "Weighted Average (External Uncertainty)");
/*  218 */       rpt.reducedChiSq = chiSq / (n - 1);
/*  219 */       rpt.criticalChiSq = criticalChiSq(n - 1, critChiSqConf, true);
/*  220 */       rpt.rejectionConfidence = 100.0D * critChiSqConf;
/*  221 */       rpt.relativeWeights = (double[])normWeight.clone();
/*  222 */       rpt.ptChiSq = new double[dataset.length];
/*  223 */       for (i = 0; i < dataset.length; i++)
/*  224 */         rpt.ptChiSq[i] = Math.pow(2.0D * (result.getValue() - 
/*  225 */             dataset[i].getValue()) / (dataset[i].getLower() + 
/*  226 */             dataset[i].getUpper()), 2.0D); 
/*  228 */       rpt.methodName = "Weighted Average";
/*  229 */     } catch (NullPointerException nullPointerException) {}
/*  234 */     if (result.gaussVariance() < Math.pow(extUnc, 2.0D) && !forceInternalUncert) {
/*  235 */       result.setLower(extUnc);
/*  236 */       result.setUpper(extUnc);
/*      */     } 
/*  239 */     return result;
/*      */   }
/*      */   
/*      */   public static final dataPt weightedAverage(dataPt[] dataset, boolean forceInternalUncert, averagingReport rpt) {
/*      */     double tmp;
/*  268 */     int n = dataset.length;
/*  271 */     Function<Double, double[]> weightCalc = mu -> {
/*      */         double[] w = new double[paramInt];
/*      */         for (int i = 0; i < paramInt; i++) {
/*      */           double dxm = paramArrayOfdataPt[i].getLower();
/*      */           double dxp = paramArrayOfdataPt[i].getUpper();
/*      */           if (dxp < 0.0D)
/*      */             dxp = 0.0D; 
/*      */           if (dxm < 0.0D)
/*      */             dxm = 0.0D; 
/*      */           double V = Math.pow(dxp + dxm, 2.0D) / 4.0D + 0.3633802276324186D * Math.pow(dxp - dxm, 2.0D) / 4.0D;
/*      */           if (V == 0.0D) {
/*      */             w[i] = 0.0D;
/*      */           } else {
/*      */             w[i] = 1.0D / V;
/*      */           } 
/*      */         } 
/*      */         return w;
/*      */       };
/*  303 */     DoubleFunction<Double> f = mu -> {
/*      */         double[] w = paramFunction.apply(Double.valueOf(mu));
/*      */         double totalWeight = 0.0D;
/*      */         double sum = 0.0D;
/*      */         for (int i = 0; i < paramInt; i++) {
/*      */           sum += w[i] * paramArrayOfdataPt[i].getValue();
/*      */           totalWeight += w[i];
/*      */         } 
/*      */         return Double.valueOf(sum / totalWeight);
/*      */       };
/*  319 */     DoubleFunction<Double> g = mu -> Double.valueOf(((Double)paramDoubleFunction.apply(mu)).doubleValue() - mu);
/*  324 */     DoubleFunction<Double> lnL = mu -> {
/*      */         double[] w = paramFunction.apply(Double.valueOf(mu));
/*      */         double sum = 0.0D;
/*      */         for (int i = 0; i < paramInt; i++)
/*      */           sum += (paramArrayOfdataPt[i].getValue() - mu) * (paramArrayOfdataPt[i].getValue() - mu) * w[i]; 
/*      */         return Double.valueOf(-0.5D * sum);
/*      */       };
/*  337 */     double[] centers = new double[n];
/*  338 */     double[] lowers = new double[n];
/*  339 */     double[] uppers = new double[n];
/*  341 */     double wtp = 0.0D, wtm = 0.0D;
/*  342 */     for (int i = 0; i < n; i++) {
/*  343 */       centers[i] = dataset[i].getValue();
/*  344 */       lowers[i] = centers[i] - 3.0D * dataset[i].getLower();
/*  345 */       uppers[i] = centers[i] + 3.0D * dataset[i].getUpper();
/*  348 */       double dxp = dataset[i].getUpper();
/*  349 */       double dxm = dataset[i].getLower();
/*      */       try {
/*  352 */         wtp += 1.0D / Math.pow(dxp, 2.0D);
/*  353 */       } catch (Exception exception) {}
/*      */       try {
/*  356 */         wtm += 1.0D / Math.pow(dxm, 2.0D);
/*  357 */       } catch (Exception exception) {}
/*      */     } 
/*  360 */     double lowerBound = MathBasicFunction.min(centers);
/*  361 */     double upperBound = MathBasicFunction.max(centers);
/*      */     try {
/*  363 */       tmp = MathBasicFunction.uniroot(g, lowerBound, upperBound);
/*  364 */     } catch (IllegalArgumentException e) {
/*  367 */       tmp = MathBasicFunction.findMax(lnL, lowerBound, upperBound);
/*      */     } 
/*  369 */     double mu_max = tmp;
/*  373 */     DoubleFunction<Double> DlnL = mu -> Double.valueOf(((Double)paramDoubleFunction.apply(mu)).doubleValue() - ((Double)paramDoubleFunction.apply(paramDouble1)).doubleValue() - 0.5D);
/*  377 */     lowerBound = MathBasicFunction.min(lowers);
/*  378 */     upperBound = MathBasicFunction.max(uppers);
/*  382 */     double upperUncert = 0.0D;
/*  383 */     double lowerUncert = 0.0D;
/*  384 */     if (wtp > 0.0D)
/*  385 */       upperUncert = Math.sqrt(1.0D / wtp); 
/*  386 */     if (wtm > 0.0D)
/*  387 */       lowerUncert = Math.sqrt(1.0D / wtm); 
/*  389 */     dataPt result = new dataPt(mu_max, upperUncert, lowerUncert, "Weighted Average");
/*  392 */     double chiSq = WeightedAveChiSq(dataset, result.getValue()) / (n - 1);
/*  393 */     double[] weights = weightCalc.apply(Double.valueOf(result.getValue()));
/*  394 */     double totWeight = MathBasicFunction.sum(weights);
/*  396 */     double[] normWeight = new double[n];
/*  398 */     double wt = 0.0D;
/*  399 */     double extUnc = 0.0D;
/*      */     int j;
/*  400 */     for (j = 0; j < n; j++) {
/*  401 */       normWeight[j] = weights[j] / totWeight;
/*  402 */       wt += weights[j];
/*  404 */       extUnc += normWeight[j] * Math.pow(dataset[j].getValue() - mu_max, 2.0D);
/*      */     } 
/*  406 */     if (n > 1) {
/*  407 */       extUnc = Math.sqrt(extUnc / (n - 1));
/*      */     } else {
/*  409 */       extUnc = 0.0D;
/*      */     } 
/*  411 */     dataPt wave_ext = new dataPt(result);
/*  414 */     wave_ext.setLower(extUnc);
/*  415 */     wave_ext.setUpper(extUnc);
/*      */     try {
/*  421 */       rpt.originalDataSet = dataset;
/*  422 */       rpt.means = new dataPt[2];
/*  423 */       rpt.means[0] = new dataPt(result);
/*  424 */       rpt.means[0].setName("Weighted Average (Internal Uncertainty)");
/*  425 */       rpt.means[1] = new dataPt(wave_ext);
/*  426 */       rpt.means[1].setName("Weighted Average (External Uncertainty)");
/*  427 */       rpt.reducedChiSq = chiSq;
/*  428 */       rpt.criticalChiSq = criticalChiSq(n - 1, critChiSqConf, true);
/*  429 */       rpt.rejectionConfidence = 100.0D * critChiSqConf;
/*  430 */       rpt.relativeWeights = (double[])normWeight.clone();
/*  431 */       rpt.ptChiSq = new double[dataset.length];
/*  432 */       for (j = 0; j < dataset.length; j++)
/*  433 */         rpt.ptChiSq[j] = Math.pow(result.getValue() - 
/*  434 */             dataset[j].getValue(), 2.0D) * weights[j]; 
/*  436 */       rpt.methodName = "Weighted Average";
/*  437 */     } catch (NullPointerException nullPointerException) {}
/*  442 */     if (result.gaussVariance() < wave_ext.gaussVariance() && !forceInternalUncert) {
/*  443 */       result.setLower(wave_ext.getLower());
/*  444 */       result.setUpper(wave_ext.getUpper());
/*      */     } 
/*  447 */     return result;
/*      */   }
/*      */   
/*      */   public static final dataPt weightedAverage(dataPt[] dataset, averagingReport rpt) {
/*  457 */     return weightedAverage(dataset, false, rpt);
/*      */   }
/*      */   
/*      */   public static final dataPt weightedAverage(dataPt[] dataset) {
/*  466 */     return weightedAverage(dataset, false, null);
/*      */   }
/*      */   
/*      */   public static final dataPt weightedAverage(dataPt[] dataset, boolean forceInternalUncert) {
/*  477 */     return weightedAverage(dataset, forceInternalUncert, null);
/*      */   }
/*      */   
/*      */   public static final double criticalChiSq(int d, double conf, boolean reduced) {
/*  502 */     int dof = Math.min(d, 340);
/*  503 */     if (previousCritChiSq == null) {
/*  504 */       previousCritChiSq = new ArrayList<>();
/*  505 */       previousCritChiSq.add(new CriticalChiSquare(dof, conf));
/*  506 */       lastCritChiSqIndex = 0;
/*  507 */       return ((CriticalChiSquare)previousCritChiSq.get(0)).getValue(reduced);
/*      */     } 
/*  509 */     CriticalChiSquare last = previousCritChiSq.get(
/*  510 */         lastCritChiSqIndex);
/*  512 */     if (last.compare(dof, conf))
/*  513 */       return last.getValue(reduced); 
/*  516 */     for (int i = 0; i < previousCritChiSq.size(); i++) {
/*  517 */       last = previousCritChiSq.get(i);
/*  518 */       if (last.compare(dof, conf)) {
/*  519 */         lastCritChiSqIndex = i;
/*  520 */         return last.getValue(reduced);
/*      */       } 
/*      */     } 
/*  525 */     previousCritChiSq.add(
/*  526 */         new CriticalChiSquare(dof, conf));
/*  527 */     lastCritChiSqIndex = 
/*  528 */       previousCritChiSq.size() - 1;
/*  529 */     return ((CriticalChiSquare)previousCritChiSq.get(
/*  530 */         lastCritChiSqIndex)).getValue(reduced);
/*      */   }
/*      */   
/*      */   public static final double criticalChiSq(int d, double conf) {
/*  541 */     return criticalChiSq(d, conf, false);
/*      */   }
/*      */   
/*      */   public static final double totalG(dataPt[] s, double x) {
/*  555 */     double sum = 0.0D;
/*  556 */     for (int i = 0; i < s.length; i++)
/*  557 */       sum += s[i].gaussian(x); 
/*  559 */     sum /= s.length;
/*  560 */     return sum;
/*      */   }
/*      */   
/*      */   public static final double EVMHypTest(dataPt[] dataset, dataPt EVM, double[] returnArray) {
/*  586 */     int n = dataset.length;
/*  588 */     double pLow = 0.0D;
/*  589 */     int lowerCount = 0;
/*  590 */     int upperCount = 0;
/*  591 */     for (int i = 0; i < n; i++) {
/*  593 */       pLow += MathSpecialFunctions.normalIntegral(dataset[i], EVM.getValue());
/*  595 */       if (dataset[i].getValue() < EVM.getValue()) {
/*  596 */         lowerCount++;
/*      */       } else {
/*  598 */         upperCount++;
/*      */       } 
/*      */     } 
/*  601 */     pLow /= n;
/*  602 */     double pHigh = 1.0D - pLow;
/*  605 */     double result = Math.pow(lowerCount - n * pLow, 2.0D) / n * pLow + 
/*  606 */       Math.pow(upperCount - n * pHigh, 2.0D) / n * pHigh;
/*      */     try {
/*  608 */       returnArray[0] = pLow;
/*  609 */       returnArray[1] = pHigh;
/*  610 */       returnArray[2] = lowerCount;
/*  611 */       returnArray[3] = upperCount;
/*  612 */       returnArray[4] = result;
/*  613 */     } catch (NullPointerException nullPointerException) {}
/*  616 */     return result;
/*      */   }
/*      */   
/*      */   public static final dataPt evm(dataPt[] dataset, averagingReport rpt) {
/*  638 */     int n = dataset.length;
/*  639 */     double[] normWeight = new double[n];
/*  641 */     double weightSum = 0.0D;
/*      */     int i;
/*  642 */     for (i = 0; i < n; i++) {
/*  643 */       normWeight[i] = totalG(dataset, dataset[i].getValue());
/*  644 */       weightSum += normWeight[i];
/*      */     } 
/*  647 */     dataPt result = new dataPt(0.0D, 0.0D, 0.0D, "Expected Value Method");
/*  648 */     for (i = 0; i < n; i++) {
/*  649 */       normWeight[i] = normWeight[i] / weightSum;
/*  651 */       result.addToValue(normWeight[i] * dataset[i].getValue());
/*  653 */       result.addToLower(Math.pow(normWeight[i] * dataset[i].getLower(), 2.0D));
/*  654 */       result.addToUpper(Math.pow(normWeight[i] * dataset[i].getUpper(), 2.0D));
/*      */     } 
/*  656 */     result.setLower(Math.sqrt(result.getLower()));
/*  657 */     result.setUpper(Math.sqrt(result.getUpper()));
/*  659 */     double extUnc = 0.0D;
/*  660 */     for (i = 0; i < n; i++)
/*  661 */       extUnc += normWeight[i] * (result.getValue() - dataset[i].getValue()) * (
/*  662 */         result.getValue() - dataset[i].getValue()); 
/*  664 */     extUnc = Math.sqrt(extUnc);
/*      */     try {
/*  667 */       rpt.originalDataSet = dataset;
/*  668 */       rpt.means = new dataPt[2];
/*  669 */       rpt.means[0] = new dataPt(result);
/*  670 */       rpt.means[0].setName("EVM (Internal Uncertainty)");
/*  671 */       rpt.means[1] = new dataPt(result.getValue(), extUnc, extUnc, 
/*  672 */           "EVM (External Uncertainty)");
/*  673 */       rpt.hypTestRpt = new double[5];
/*  674 */       rpt.hypTest = EVMHypTest(dataset, result, rpt.hypTestRpt);
/*  676 */       rpt.hypTest = 1.0D - MathSpecialFunctions.erf(Math.sqrt(0.5D * rpt.hypTest));
/*  677 */       rpt.relativeWeights = (double[])normWeight.clone();
/*  678 */       rpt.methodName = "Expected Value Method";
/*  679 */     } catch (NullPointerException nullPointerException) {}
/*  684 */     if (result.gaussVariance() < Math.pow(extUnc, 2.0D)) {
/*  685 */       result.setLower(extUnc);
/*  686 */       result.setUpper(extUnc);
/*      */     } 
/*  689 */     return result;
/*      */   }
/*      */   
/*      */   public static final dataPt evm(dataPt[] dataset) {
/*  698 */     return evm(dataset, null);
/*      */   }
/*      */   
/*      */   public static final double[] calcSigmaSqWeights(dataPt[] dataset, boolean normalize) {
/*  717 */     int n = dataset.length;
/*  718 */     double[] result = new double[n];
/*  719 */     double weightSum = 0.0D;
/*      */     int i;
/*  721 */     for (i = 0; i < n; i++) {
/*  722 */       result[i] = 1.0D / dataset[i].gaussVariance();
/*  723 */       weightSum += result[i];
/*      */     } 
/*  726 */     if (normalize)
/*  727 */       for (i = 0; i < n; i++)
/*  728 */         result[i] = result[i] / weightSum;  
/*  732 */     return result;
/*      */   }
/*      */   
/*      */   public static final dataPt findPresValue(dataPt[] dataset, double meanVal) {
/*  751 */     dataPt result = new dataPt(dataset[0]);
/*  752 */     for (int i = 1; i < dataset.length; i++) {
/*  753 */       if (result.gaussVariance() > dataset[i].gaussVariance()) {
/*  755 */         result = new dataPt(dataset[i]);
/*  756 */       } else if (result.gaussVariance() == dataset[i].gaussVariance() && 
/*  757 */         Math.abs(result.getValue() - meanVal) < 
/*  758 */         Math.abs(dataset[i].getValue() - meanVal)) {
/*  760 */         result = new dataPt(dataset[i]);
/*      */       } 
/*      */     } 
/*  764 */     return result;
/*      */   }
/*      */   
/*      */   public static final boolean askRemove(String method, dataPt d, String avgMethodName) {
/*  780 */     String title = String.valueOf(method) + " - Outlier for using " + avgMethodName;
/*  781 */     String message = "Data point #" + d.toString() + "\n";
/*  782 */     message = String.valueOf(message) + " has been marked as an outlier by " + method + 
/*  783 */       "'s criterion in " + avgMethodName + ". \n Exclude from the analysis using " + avgMethodName + "?";
/*  784 */     int answer = JOptionPane.showConfirmDialog(null, message, title, 0, 3);
/*  785 */     return (answer == 0);
/*      */   }
/*      */   
/*      */   public static final boolean askRemove(String method, dataPt d) {
/*  792 */     String title = String.valueOf(method) + " - Outlier";
/*  793 */     String message = "Data point #" + d.toString() + "\n";
/*  794 */     message = String.valueOf(message) + " has been marked as an outlier by " + method + 
/*  795 */       "'s criterion . \n Exclude from the analysis?";
/*  796 */     int answer = JOptionPane.showConfirmDialog(null, message, title, 0, 3);
/*  797 */     return (answer == 0);
/*      */   }
/*      */   
/*      */   private static boolean askAdoptUnWt() {
/*  811 */     String title = "Adopt unweighted mean?";
/*  812 */     String message = "Warning! The LWM weighted mean does not overlap the unweighted mean. The method perscribes adoption of the unweighted mean. Would you like to adopt the unweighted mean?";
/*  813 */     int answer = JOptionPane.showConfirmDialog(null, message, title, 0, 3);
/*  814 */     return (answer == 0);
/*      */   }
/*      */   
/*      */   public static final boolean dataPtInArray(dataPt needle, dataPt[] haystack, boolean compareNames) {
/*  832 */     for (int i = 0; i < haystack.length; i++) {
/*  833 */       if (needle.equals(haystack[i], compareNames))
/*  834 */         return true; 
/*      */     } 
/*  837 */     return false;
/*      */   }
/*      */   
/*      */   public static final boolean dataPtInArray(dataPt needle, dataPt[] haystack) {
/*  847 */     return dataPtInArray(needle, haystack, false);
/*      */   }
/*      */   
/*      */   public static final dataPt lwm(dataPt[] dataset, double weightLimit, int outlierMethod, double confidenceLevel, averagingReport rpt) {
/*      */     dataPt[] effectiveDataSet;
/*  895 */     String[] methods = { "Chauvenet", "Peirce", "Modified Peirce", "Birch" };
/*  896 */     double epsilon = 1.0E-5D;
/*  917 */     int n = dataset.length;
/*  918 */     dataPt[] outliers = new dataPt[0];
/*  919 */     if (n > 2)
/*  920 */       if (outlierMethod == 0) {
/*  921 */         outliers = outlierMethods.ChauvenetCriterion(dataset);
/*  922 */       } else if (outlierMethod == 1) {
/*  923 */         outliers = outlierMethods.PeirceCriterion(dataset);
/*  924 */       } else if (outlierMethod == 2) {
/*  925 */         outliers = outlierMethods.ModifiedPeirceCriterion(dataset);
/*  926 */       } else if (outlierMethod == 3) {
/*  927 */         outliers = outlierMethods.BirchCriterion(dataset);
/*      */       }  
/*  930 */     List<dataPt> outliersList = new ArrayList<>();
/*      */     int i;
/*  931 */     for (i = 0; i < outliers.length; i++) {
/*  932 */       if (askRemove(methods[outlierMethod], outliers[i], "LWM"))
/*  933 */         outliersList.add(outliers[i]); 
/*      */     } 
/*  936 */     if (outliers.length > 0) {
/*  937 */       List<dataPt> effectiveDataSetList = new ArrayList<>();
/*  938 */       for (i = 0; i < n; i++) {
/*  939 */         if (!outliersList.contains(dataset[i]))
/*  940 */           effectiveDataSetList.add(dataset[i]); 
/*      */       } 
/*  943 */       effectiveDataSet = effectiveDataSetList.<dataPt>toArray(new dataPt[0]);
/*  944 */       n = effectiveDataSet.length;
/*      */     } else {
/*  946 */       effectiveDataSet = dataset;
/*      */     } 
/*  948 */     averagingReport wtRpt = new averagingReport();
/*  949 */     dataPt weightedMean = weightedAverage(effectiveDataSet, wtRpt);
/*  950 */     double redChiSq = wtRpt.reducedChiSq;
/*  951 */     double ReducedCritChiSq = criticalChiSq(n - 1, confidenceLevel / 100.0D, true);
/*  952 */     if (redChiSq < ReducedCritChiSq) {
/*  953 */       dataPt dataPt1 = new dataPt(weightedMean);
/*  954 */       dataPt1.setName("LWM");
/*      */       try {
/*  958 */         rpt.outliers = outliersList.<dataPt>toArray(new dataPt[0]);
/*  959 */         rpt.relativeWeights = (double[])wtRpt.relativeWeights.clone();
/*  960 */         rpt.originalDataSet = (dataPt[])dataset.clone();
/*  961 */         rpt.adjustedDataSet = (dataPt[])effectiveDataSet.clone();
/*  962 */         rpt.reducedChiSq = redChiSq;
/*  963 */         rpt.criticalChiSq = ReducedCritChiSq;
/*  964 */         rpt.rejectionConfidence = confidenceLevel;
/*  965 */         rpt.means = (dataPt[])wtRpt.means.clone();
/*  966 */         rpt.means[0].setName("LWM (Internal Uncertainty)");
/*  967 */         rpt.means[1].setName("LWM (External Uncertainty)");
/*  968 */         rpt.ptChiSq = (double[])wtRpt.ptChiSq.clone();
/*  969 */         rpt.methodName = "Limitation of Statistical Weights";
/*  970 */       } catch (NullPointerException nullPointerException) {}
/*  973 */       return dataPt1;
/*      */     } 
/*  976 */     List<Integer> pointsChangedList = new ArrayList<>();
/*  977 */     boolean leaveLoop = false;
/*  978 */     while (!leaveLoop) {
/*  979 */       double[] normWeight = calcSigmaSqWeights(effectiveDataSet, true);
/*  980 */       double[] regWeight = calcSigmaSqWeights(effectiveDataSet, false);
/*  981 */       double weightSum = MathBasicFunction.sum(regWeight);
/*  983 */       leaveLoop = true;
/*  984 */       for (i = 0; i < n; i++) {
/*  985 */         if (normWeight[i] - weightLimit > 1.0E-5D) {
/*  987 */           if (!pointsChangedList.contains(Integer.valueOf(i)))
/*  988 */             pointsChangedList.add(Integer.valueOf(i)); 
/*  990 */           leaveLoop = false;
/*  991 */           double adjRatio = weightLimit * (weightSum - regWeight[i]) / 
/*  992 */             regWeight[i] * (1.0D - weightLimit);
/*  993 */           effectiveDataSet[i].setLower(effectiveDataSet[i].getLower() / 
/*  994 */               Math.sqrt(adjRatio));
/*  995 */           effectiveDataSet[i].setUpper(effectiveDataSet[i].getUpper() / 
/*  996 */               Math.sqrt(adjRatio));
/*      */           break;
/*      */         } 
/*      */       } 
/*      */     } 
/* 1002 */     weightedMean = weightedAverage(effectiveDataSet, wtRpt);
/* 1003 */     averagingReport uwtRpt = new averagingReport();
/* 1004 */     dataPt unWeightedMean = unweightedAverage(effectiveDataSet, uwtRpt);
/* 1005 */     redChiSq = wtRpt.reducedChiSq;
/* 1010 */     if (!weightedMean.overlaps(unWeightedMean) && redChiSq > ReducedCritChiSq && 
/* 1011 */       askAdoptUnWt()) {
/* 1012 */       dataPt dataPt1 = new dataPt(unWeightedMean);
/* 1013 */       dataPt1.setName("LWM");
/*      */       try {
/* 1016 */         rpt.outliers = outliersList.<dataPt>toArray(new dataPt[0]);
/* 1017 */         rpt.originalDataSet = (dataPt[])dataset.clone();
/* 1018 */         rpt.adjustedDataSet = (dataPt[])effectiveDataSet.clone();
/* 1019 */         rpt.differenceFromMeanSq = (double[])uwtRpt.differenceFromMeanSq.clone();
/* 1020 */         rpt.useUnweightedMean = true;
/* 1021 */         rpt.changedPoints = pointsChangedList.<Integer>toArray(new Integer[0]);
/* 1022 */         rpt.means = new dataPt[1];
/* 1023 */         rpt.means[0] = new dataPt(dataPt1);
/* 1024 */         rpt.methodName = "Limitation of Statistical Weights";
/* 1025 */       } catch (NullPointerException nullPointerException) {}
/* 1028 */       return dataPt1;
/*      */     } 
/* 1032 */     dataPt result = new dataPt(weightedMean);
/* 1033 */     result.setName("LWM");
/* 1034 */     dataPt mostPresVal = findPresValue(dataset, result.getValue());
/*      */     try {
/* 1037 */       rpt.outliers = outliersList.<dataPt>toArray(new dataPt[0]);
/* 1038 */       rpt.relativeWeights = (double[])wtRpt.relativeWeights.clone();
/* 1039 */       rpt.originalDataSet = (dataPt[])dataset.clone();
/* 1040 */       rpt.adjustedDataSet = (dataPt[])effectiveDataSet.clone();
/* 1041 */       rpt.reducedChiSq = redChiSq;
/* 1042 */       rpt.criticalChiSq = ReducedCritChiSq;
/* 1043 */       rpt.rejectionConfidence = confidenceLevel;
/* 1044 */       rpt.means = (dataPt[])wtRpt.means.clone();
/* 1045 */       rpt.means[0].setName("LWM (Internal Uncertainty)");
/* 1046 */       rpt.means[1].setName("LWM (External Uncertainty)");
/* 1047 */       rpt.ptChiSq = (double[])wtRpt.ptChiSq.clone();
/* 1048 */       rpt.changedPoints = pointsChangedList.<Integer>toArray(new Integer[0]);
/* 1049 */       rpt.methodName = "Limitation of Statostical Weights";
/* 1050 */     } catch (NullPointerException nullPointerException) {}
/* 1054 */     if (!result.overlaps(mostPresVal) && redChiSq > ReducedCritChiSq) {
/* 1055 */       if (result.getValue() < mostPresVal.getValue()) {
/* 1056 */         result.setUpper(Math.abs(result.getValue() - mostPresVal.getValue() - 
/* 1057 */               mostPresVal.getLower()));
/* 1058 */         result.setLower(result.getUpper());
/*      */       } else {
/* 1060 */         result.setLower(Math.abs(result.getValue() - mostPresVal.getValue() + 
/* 1061 */               mostPresVal.getUpper()));
/* 1062 */         result.setUpper(result.getLower());
/*      */       } 
/*      */       try {
/* 1066 */         rpt.means = new dataPt[3];
/* 1067 */         rpt.means[0] = new dataPt(wtRpt.means[0]);
/* 1068 */         rpt.means[1] = new dataPt(wtRpt.means[1]);
/* 1069 */         rpt.means[2] = new dataPt(result);
/* 1070 */         rpt.means[0].setName("LWM (Internal Uncertainty)");
/* 1071 */         rpt.means[1].setName("LWM (External Uncertainty)");
/* 1072 */         rpt.means[2].setName("LWM (Uncertainty increased to overlap most precise value)");
/* 1073 */         rpt.methodName = "Limitation of Statistical Weights";
/* 1074 */       } catch (NullPointerException nullPointerException) {}
/*      */     } 
/* 1078 */     return result;
/*      */   }
/*      */   
/*      */   public static final dataPt lwm(dataPt[] dataset) {
/* 1087 */     return lwm(dataset, 0.5D, 0, 99.0D, null);
/*      */   }
/*      */   
/*      */   public static final dataPt lwm(dataPt[] dataset, averagingReport rpt) {
/* 1097 */     return lwm(dataset, 0.5D, 0, 99.0D, rpt);
/*      */   }
/*      */   
/*      */   public static final dataPt lwm(dataPt[] dataset, int outlierMethod) {
/* 1108 */     return lwm(dataset, 0.5D, outlierMethod, 99.0D, null);
/*      */   }
/*      */   
/*      */   public static final dataPt lwm(dataPt[] dataset, double confidenceLevel) {
/* 1119 */     return lwm(dataset, 0.5D, 0, confidenceLevel, null);
/*      */   }
/*      */   
/*      */   public static final dataPt lwm(dataPt[] dataset, int outlierMethod, double confidenceLevel) {
/* 1132 */     return lwm(dataset, 0.5D, outlierMethod, confidenceLevel, null);
/*      */   }
/*      */   
/*      */   public static final dataPt lwm(dataPt[] dataset, int outlierMethod, averagingReport rpt) {
/* 1145 */     return lwm(dataset, 0.5D, outlierMethod, 99.0D, rpt);
/*      */   }
/*      */   
/*      */   public static final dataPt lwm(dataPt[] dataset, double confidenceLevel, averagingReport rpt) {
/* 1158 */     return lwm(dataset, 0.5D, 0, confidenceLevel, rpt);
/*      */   }
/*      */   
/*      */   public static final dataPt lwm(dataPt[] dataset, int outlierMethod, double confidenceLevel, averagingReport rpt) {
/* 1172 */     return lwm(dataset, 0.5D, outlierMethod, confidenceLevel, rpt);
/*      */   }
/*      */   
/*      */   public static final double[] CalcNormalizedResiduals(dataPt[] dataset, double[] weights, double mean) {
/* 1193 */     double[] result = new double[dataset.length];
/* 1194 */     double weightSum = MathBasicFunction.sum(weights);
/* 1195 */     for (int i = 0; i < result.length; i++)
/* 1196 */       result[i] = Math.sqrt(weights[i] * weightSum / (
/* 1197 */           weightSum - weights[i])) * (dataset[i].getValue() - mean); 
/* 1199 */     return result;
/*      */   }
/*      */   
/*      */   public static final dataPt nrm(dataPt[] dataset, double confidenceLevel, averagingReport rpt) {
/* 1234 */     int n = dataset.length;
/* 1235 */     dataPt[] effectiveDataSet = new dataPt[n];
/* 1237 */     double outlierProbability = 100.0D * (1.0D - confidenceLevel);
/* 1238 */     if (outlierProbability > n)
/* 1239 */       outlierProbability = n; 
/* 1242 */     double criticalR = Math.sqrt(1.8D * Math.log(n / outlierProbability) + 
/* 1243 */         2.6D);
/*      */     int i;
/* 1245 */     for (i = 0; i < n; i++)
/* 1246 */       effectiveDataSet[i] = new dataPt(dataset[i]); 
/* 1249 */     double[] weights = calcSigmaSqWeights(effectiveDataSet, false);
/* 1250 */     double weightSum = MathBasicFunction.sum(weights);
/* 1251 */     dataPt result = weightedAverage(effectiveDataSet);
/* 1253 */     double[] normResid = CalcNormalizedResiduals(effectiveDataSet, weights, result.getValue());
/* 1255 */     boolean leaveLoop = false;
/* 1256 */     List<Integer> pointsChangedList = new ArrayList<>();
/* 1257 */     int iterationCount = 0;
/* 1258 */     while (!leaveLoop) {
/* 1259 */       leaveLoop = true;
/* 1260 */       arrayMaxMin maxNormResid = new arrayMaxMin(MathBasicFunction.abs(normResid));
/* 1263 */       if (maxNormResid.max > criticalR) {
/* 1264 */         leaveLoop = false;
/* 1265 */         i = maxNormResid.maxInd;
/* 1266 */         if (!pointsChangedList.contains(Integer.valueOf(i)))
/* 1267 */           pointsChangedList.add(Integer.valueOf(i)); 
/* 1269 */         double adjRatio = 1.0D - weightSum * (Math.pow(normResid[i], 2.0D) - 
/* 1270 */           Math.pow(criticalR, 2.0D)) / (weightSum * 
/* 1271 */           Math.pow(normResid[i], 2.0D) - weights[i] * 
/* 1272 */           Math.pow(criticalR, 2.0D));
/* 1275 */         weights[i] = weights[i] * adjRatio;
/* 1276 */         effectiveDataSet[i].setLower(effectiveDataSet[i].getLower() / 
/* 1277 */             Math.sqrt(adjRatio));
/* 1278 */         effectiveDataSet[i].setUpper(effectiveDataSet[i].getUpper() / 
/* 1279 */             Math.sqrt(adjRatio));
/* 1281 */         weightSum = MathBasicFunction.sum(weights);
/* 1282 */         result = weightedAverage(effectiveDataSet);
/* 1283 */         normResid = CalcNormalizedResiduals(effectiveDataSet, weights, 
/* 1284 */             result.getValue());
/*      */       } 
/* 1287 */       iterationCount++;
/* 1288 */       if (iterationCount > 5000)
/* 1289 */         leaveLoop = true; 
/*      */     } 
/* 1293 */     averagingReport wtRpt = new averagingReport();
/* 1294 */     result = weightedAverage(effectiveDataSet, wtRpt);
/* 1295 */     result.setName("NRM");
/*      */     try {
/* 1298 */       rpt.relativeWeights = (double[])wtRpt.relativeWeights.clone();
/* 1299 */       rpt.originalDataSet = (dataPt[])dataset.clone();
/* 1300 */       rpt.adjustedDataSet = (dataPt[])effectiveDataSet.clone();
/* 1301 */       rpt.normalizedResiduals = (double[])normResid.clone();
/* 1302 */       rpt.reducedChiSq = wtRpt.reducedChiSq;
/* 1303 */       rpt.criticalChiSq = criticalChiSq(n - 1, critChiSqConf, true);
/* 1304 */       rpt.rejectionConfidence = 100.0D * critChiSqConf;
/* 1305 */       rpt.means = (dataPt[])wtRpt.means.clone();
/* 1306 */       rpt.means[0].setName("NRM (Internal Uncertainty)");
/* 1307 */       rpt.means[1].setName("NRM (External Uncertainty)");
/* 1308 */       rpt.ptChiSq = (double[])wtRpt.ptChiSq.clone();
/* 1309 */       rpt.changedPoints = pointsChangedList.<Integer>toArray(new Integer[0]);
/* 1310 */       rpt.methodName = "Normalized Residuals Method";
/* 1311 */     } catch (NullPointerException nullPointerException) {}
/* 1314 */     return result;
/*      */   }
/*      */   
/*      */   public static final dataPt nrm(dataPt[] dataset, averagingReport rpt) {
/* 1325 */     return nrm(dataset, 0.99D, rpt);
/*      */   }
/*      */   
/*      */   public static final dataPt nrm(dataPt[] dataset, double confidenceLevel) {
/* 1336 */     return nrm(dataset, confidenceLevel, null);
/*      */   }
/*      */   
/*      */   public static final dataPt nrm(dataPt[] dataset) {
/* 1346 */     return nrm(dataset, 0.99D, null);
/*      */   }
/*      */   
/*      */   public static final dataPt rt(dataPt[] dataset, int outlierConfidenceLevel, averagingReport rpt) {
/* 1389 */     dataPt stdNorm = new dataPt(0.0D, 1.0D, 1.0D, "Standard Normal");
/* 1391 */     int n = dataset.length;
/* 1394 */     double[] outlyingStat = new double[n];
/* 1395 */     List<dataPt> outliersList = new ArrayList<>();
/* 1396 */     List<dataPt> effectiveDataSetList = new ArrayList<>();
/* 1397 */     dataPt unweightedMean = unweightedAverage(dataset);
/*      */     int i;
/* 1398 */     for (i = 0; i < n; i++) {
/* 1400 */       if (n - outliersList.size() < 4)
/*      */         break; 
/* 1404 */       double reducedMean = unweightedMean.getValue() * n / (n - 1) - 
/* 1405 */         dataset[i].getValue() / (n - 1);
/* 1407 */       double reducedSD = Math.sqrt(n / (n - 2) * unweightedMean.gaussVariance() - 
/* 1408 */           n * (unweightedMean.getValue() - dataset[i].getValue()) * (
/* 1409 */           unweightedMean.getValue() - dataset[i].getValue()) / ((
/* 1410 */           n - 1) * (n - 1) * (n - 2)));
/* 1411 */       outlyingStat[i] = (dataset[i].getValue() - reducedMean) / 
/* 1412 */         Math.sqrt(dataset[i].gaussVariance() + reducedSD * reducedSD);
/* 1414 */       if (Math.abs(outlyingStat[i]) > 1.96D * outlierConfidenceLevel && 
/* 1415 */         askRemove("Rajeval Technique", dataset[i], "RT"))
/* 1416 */         outliersList.add(dataset[i]); 
/*      */     } 
/* 1420 */     for (i = 0; i < n; i++) {
/* 1423 */       if (!outliersList.contains(dataset[i]))
/* 1424 */         effectiveDataSetList.add(new dataPt(dataset[i])); 
/*      */     } 
/* 1427 */     dataPt[] effectiveDataSet = effectiveDataSetList.<dataPt>toArray(new dataPt[0]);
/* 1428 */     n = effectiveDataSet.length;
/* 1429 */     List<Integer> pointsChangedList = new ArrayList<>();
/* 1430 */     boolean leaveLoop = false;
/* 1431 */     double criticalIncons = Math.pow(0.5D, n / (n - 1));
/* 1432 */     while (!leaveLoop) {
/* 1436 */       dataPt weightedMean = weightedAverage(effectiveDataSet, true);
/* 1437 */       leaveLoop = true;
/* 1438 */       for (i = 0; i < n; i++) {
/* 1439 */         double inconsistantStatistic = (effectiveDataSet[i].getValue() - 
/* 1440 */           weightedMean.getValue()) / Math.sqrt(effectiveDataSet[i].gaussVariance() - 
/* 1441 */             weightedMean.gaussVariance());
/* 1442 */         if (Math.abs(MathSpecialFunctions.normalIntegral(stdNorm, inconsistantStatistic) - 
/* 1443 */             0.5D) > criticalIncons) {
/* 1444 */           if (!pointsChangedList.contains(Integer.valueOf(i)))
/* 1445 */             pointsChangedList.add(Integer.valueOf(i)); 
/* 1447 */           leaveLoop = false;
/* 1449 */           effectiveDataSet[i].setLower(Math.sqrt(effectiveDataSet[i].getLower() * 
/* 1450 */                 effectiveDataSet[i].getLower() + weightedMean.getLower() * 
/* 1451 */                 weightedMean.getLower()));
/* 1452 */           effectiveDataSet[i].setUpper(Math.sqrt(effectiveDataSet[i].getUpper() * 
/* 1453 */                 effectiveDataSet[i].getUpper() + weightedMean.getUpper() * 
/* 1454 */                 weightedMean.getUpper()));
/*      */         } 
/*      */       } 
/*      */     } 
/* 1458 */     averagingReport wtRpt = new averagingReport();
/* 1459 */     dataPt result = weightedAverage(effectiveDataSet, wtRpt);
/* 1460 */     result.setName("RT");
/*      */     try {
/* 1464 */       rpt.relativeWeights = (double[])wtRpt.relativeWeights.clone();
/* 1465 */       rpt.originalDataSet = (dataPt[])dataset.clone();
/* 1466 */       rpt.adjustedDataSet = (dataPt[])effectiveDataSet.clone();
/* 1467 */       rpt.reducedChiSq = wtRpt.reducedChiSq;
/* 1468 */       rpt.criticalChiSq = criticalChiSq(n - 1, critChiSqConf, true);
/* 1469 */       rpt.rejectionConfidence = 100.0D * critChiSqConf;
/* 1470 */       rpt.means = (dataPt[])wtRpt.means.clone();
/* 1471 */       rpt.means[0].setName("RT (Internal Uncertainty)");
/* 1472 */       rpt.means[1].setName("RT (External Uncertainty)");
/* 1473 */       rpt.ptChiSq = (double[])wtRpt.ptChiSq.clone();
/* 1474 */       rpt.changedPoints = pointsChangedList.<Integer>toArray(new Integer[0]);
/* 1475 */       rpt.outliers = outliersList.<dataPt>toArray(new dataPt[0]);
/* 1476 */       rpt.methodName = "Rajeval Technique";
/* 1477 */     } catch (NullPointerException nullPointerException) {}
/* 1480 */     return result;
/*      */   }
/*      */   
/*      */   public static final dataPt rt(dataPt[] dataset, averagingReport rpt) {
/* 1491 */     return rt(dataset, 2, rpt);
/*      */   }
/*      */   
/*      */   public static final dataPt rt(dataPt[] dataset, int outlierConfidenceLevel) {
/* 1502 */     return rt(dataset, outlierConfidenceLevel, null);
/*      */   }
/*      */   
/*      */   public static final dataPt rt(dataPt[] dataset) {
/* 1512 */     return rt(dataset, 2, null);
/*      */   }
/*      */   
/*      */   public static final double median(double[] x) {
/* 1525 */     int n = x.length;
/* 1526 */     Arrays.sort(x);
/* 1527 */     if (n % 2 == 0)
/* 1528 */       return 0.5D * (x[n / 2] + x[n / 2 - 1]); 
/* 1531 */     n = (int)Math.floor(0.5D * n);
/* 1532 */     return x[n];
/*      */   }
/*      */   
/*      */   public static final double median(dataPt[] dataset) {
/* 1547 */     int n = dataset.length;
/* 1548 */     double[] temp = new double[n];
/* 1549 */     for (int i = 0; i < n; i++)
/* 1550 */       temp[i] = dataset[i].getValue(); 
/* 1552 */     return median(temp);
/*      */   }
/*      */   
/*      */   public static final double estimateVariance(double[] x, double mean) {
/* 1567 */     int n = x.length;
/* 1568 */     double result = 0.0D;
/* 1569 */     for (int i = 0; i < n; i++)
/* 1570 */       result += (x[i] - mean) * (x[i] - mean); 
/* 1572 */     result /= (n - 1);
/* 1573 */     return result;
/*      */   }
/*      */   
/*      */   public static final dataPt bootstrap(dataPt[] dataset, int NUM_MEDIANS, averagingReport rpt) {
/* 1598 */     int n = dataset.length;
/* 1600 */     double[] medians = new double[NUM_MEDIANS];
/* 1601 */     double[] sampleData = new double[n];
/* 1602 */     for (int i = 0; i < NUM_MEDIANS; i++) {
/* 1603 */       int[] sampleSeq = statSampling.rInt(n, 0, n);
/* 1604 */       for (int j = 0; j < n; j++) {
/* 1605 */         dataPt temp = dataset[sampleSeq[j]];
/* 1606 */         sampleData[j] = statSampling.rAnorm(temp.getValue(), 
/* 1607 */             temp.getLower(), temp.getUpper());
/*      */       } 
/* 1609 */       medians[i] = median(sampleData);
/*      */     } 
/* 1611 */     double mean = MathBasicFunction.sum(medians) / medians.length;
/* 1612 */     double uncertainty = Math.sqrt(estimateVariance(medians, mean));
/* 1613 */     dataPt result = new dataPt(mean, uncertainty, uncertainty, "Bootstrap");
/*      */     try {
/* 1616 */       rpt.originalDataSet = (dataPt[])dataset.clone();
/* 1617 */       rpt.means = new dataPt[1];
/* 1618 */       rpt.means[0] = result;
/* 1619 */       rpt.reducedChiSq = WeightedAveChiSq(dataset, result.getValue()) / (
/* 1620 */         n - 1);
/* 1621 */       rpt.bootstrap_NUM_MEDIANS = NUM_MEDIANS;
/* 1622 */       rpt.methodName = "Bootstrap";
/* 1623 */     } catch (NullPointerException nullPointerException) {}
/* 1626 */     return result;
/*      */   }
/*      */   
/*      */   public static final dataPt bootstrap(dataPt[] dataset, averagingReport rpt) {
/* 1637 */     return bootstrap(dataset, 800000, rpt);
/*      */   }
/*      */   
/*      */   public static final dataPt bootstrap(dataPt[] dataset) {
/* 1647 */     return bootstrap(dataset, 800000, null);
/*      */   }
/*      */   
/*      */   public static final dataPt bootstrap(dataPt[] dataset, int NUM_MEDIANS) {
/* 1658 */     return bootstrap(dataset, NUM_MEDIANS, null);
/*      */   }
/*      */   
/*      */   private static double[] mpWeights(dataPt[] dataset, double y) {
/* 1674 */     int n = dataset.length;
/* 1675 */     double[] result = new double[n];
/* 1676 */     for (int i = 0; i < n; i++)
/* 1677 */       result[i] = 1.0D / (y + dataset[i].gaussVariance()); 
/* 1680 */     return result;
/*      */   }
/*      */   
/*      */   private static double weightedSum(dataPt[] dataset, double[] weights) {
/* 1695 */     int n = dataset.length;
/* 1696 */     double[] temp = new double[n];
/* 1697 */     for (int i = 0; i < n; i++)
/* 1698 */       temp[i] = dataset[i].getValue(); 
/* 1700 */     return MathBasicFunction.weightedSum(temp, weights);
/*      */   }
/*      */   
/*      */   private static double mpFunction(dataPt[] dataset, double y) {
/* 1717 */     int n = dataset.length;
/* 1718 */     double[] weights = mpWeights(dataset, y);
/* 1719 */     double mean = weightedSum(dataset, weights);
/* 1721 */     double result = 0.0D;
/* 1722 */     for (int i = 0; i < n; i++)
/* 1723 */       result += weights[i] * (dataset[i].getValue() - mean) * (
/* 1724 */         dataset[i].getValue() - mean); 
/* 1726 */     result -= (n - 1);
/* 1727 */     return result;
/*      */   }
/*      */   
/*      */   public static final dataPt mp(dataPt[] dataset, double precision, int maxIt, averagingReport rpt) {
/* 1755 */     int n = dataset.length;
/* 1756 */     double yLower = 0.0D;
/* 1757 */     double fLower = mpFunction(dataset, yLower);
/* 1759 */     double yMid = 0.0D;
/* 1760 */     if (fLower < 0.0D) {
/* 1762 */       yMid = 0.0D;
/*      */     } else {
/* 1764 */       dataPt unweightedMean = unweightedAverage(dataset);
/* 1767 */       double yUpper = n * unweightedMean.gaussVariance();
/* 1768 */       double fUpper = mpFunction(dataset, yUpper);
/* 1770 */       if (fUpper > 0.0D) {
/* 1771 */         yLower = yUpper;
/* 1772 */         while (fUpper > 0.0D) {
/* 1773 */           yUpper *= 1.1D;
/* 1774 */           fUpper = mpFunction(dataset, yUpper);
/*      */         } 
/*      */       } 
/* 1778 */       for (int i = 1; i <= maxIt; i++) {
/* 1779 */         yMid = 0.5D * (yLower + yUpper);
/* 1780 */         double fMid = mpFunction(dataset, yMid);
/* 1782 */         if (Math.abs(fMid) < precision)
/*      */           break; 
/* 1784 */         if (fMid < 0.0D) {
/* 1785 */           yUpper = yMid;
/*      */         } else {
/* 1787 */           yLower = yMid;
/*      */         } 
/* 1789 */         if (i == maxIt)
/* 1790 */           JOptionPane.showMessageDialog(null, "Warning! Bisection Algorithm for Mandel Paule method failed, result may not be optimal. Increase the maximum number of iterations to attain a better result."); 
/*      */       } 
/*      */     } 
/* 1795 */     double[] weights = mpWeights(dataset, yMid);
/* 1796 */     dataPt result = new dataPt();
/* 1797 */     result.setName("Mandel-Paule");
/* 1798 */     result.setValue(weightedSum(dataset, weights));
/* 1800 */     dataPt weightedMean = weightedAverage(dataset);
/* 1803 */     if (yMid > weightedMean.gaussVariance()) {
/* 1804 */       result.setLower(Math.sqrt(yMid));
/* 1805 */       result.setUpper(Math.sqrt(yMid));
/*      */     } else {
/* 1807 */       result.setLower(weightedMean.getLower());
/* 1808 */       result.setUpper(weightedMean.getUpper());
/*      */     } 
/*      */     try {
/* 1812 */       rpt.originalDataSet = (dataPt[])dataset.clone();
/* 1813 */       rpt.means = new dataPt[1];
/* 1814 */       rpt.means[0] = result;
/* 1815 */       rpt.reducedChiSq = WeightedAveChiSq(dataset, result.getValue()) / (
/* 1816 */         n - 1);
/* 1817 */       double weightSum = MathBasicFunction.sum(weights);
/* 1818 */       rpt.relativeWeights = new double[n];
/* 1819 */       for (int i = 0; i < n; i++)
/* 1820 */         rpt.relativeWeights[i] = weights[i] / weightSum; 
/* 1822 */       rpt.methodName = "Mandel-Paule Method";
/* 1823 */     } catch (NullPointerException nullPointerException) {}
/* 1826 */     return result;
/*      */   }
/*      */   
/*      */   public static final dataPt mp(dataPt[] dataset, averagingReport rpt) {
/* 1840 */     return mp(dataset, 1.0E-12D, 1000, rpt);
/*      */   }
/*      */   
/*      */   public static final dataPt mp(dataPt[] dataset, double precision, int maxIt) {
/* 1855 */     return mp(dataset, precision, maxIt, null);
/*      */   }
/*      */   
/*      */   public static final dataPt mp(dataPt[] dataset) {
/* 1867 */     return mp(dataset, 1.0E-12D, 1000, null);
/*      */   }
/*      */   
/*      */   public static final dataPt consistanMinimumVarianceMethod(dataPt[] dataset, double p) {
/* 1884 */     int MAXSTEPS = 1000;
/* 1885 */     double precision = Math.sqrt(Math.nextUp(0.0D));
/* 1891 */     int n = dataset.length;
/* 1893 */     double lower = dataset[0].getValue();
/* 1894 */     double upper = dataset[0].getValue();
/* 1895 */     double minVar = dataset[0].gaussVariance();
/*      */     int i;
/* 1897 */     for (i = 1; i < n; i++) {
/* 1898 */       if (dataset[i].getValue() > upper) {
/* 1899 */         upper = dataset[i].getValue();
/* 1900 */       } else if (dataset[i].getValue() < lower) {
/* 1901 */         lower = dataset[i].getValue();
/*      */       } 
/* 1903 */       if (dataset[i].gaussVariance() < minVar)
/* 1904 */         minVar = dataset[i].gaussVariance(); 
/*      */     } 
/* 1907 */     double mean = 0.0D;
/* 1910 */     for (i = 0; i < 1000 && 
/* 1911 */       upper - lower >= precision; i++) {
/* 1914 */       double lowerThird = lower + (upper - lower) / 3.0D;
/* 1915 */       double upperThird = upper - (upper - lower) / 3.0D;
/* 1917 */       if (outlierMethods.consistantVariance(lowerThird, dataset, p) > 
/* 1918 */         outlierMethods.consistantVariance(upperThird, dataset, p)) {
/* 1919 */         lower = lowerThird;
/*      */       } else {
/* 1921 */         upper = upperThird;
/*      */       } 
/* 1923 */       mean = 0.5D * (upper + lower);
/*      */     } 
/* 1927 */     double variance = outlierMethods.consistantVariance(mean, dataset, p);
/* 1929 */     if (variance < 0.0D)
/* 1930 */       variance = minVar; 
/* 1933 */     dataPt result = new dataPt(mean, Math.sqrt(variance), Math.sqrt(variance));
/* 1935 */     return result;
/*      */   }
/*      */ }


/* Location:              D:\X\ND\ENSDF\AverageTool_22January2025.jar!\averagingAlgorithms\averagingMethods.class
 * Java compiler version: 8 (52.0)
 * JD-Core Version:       1.1.3
 */