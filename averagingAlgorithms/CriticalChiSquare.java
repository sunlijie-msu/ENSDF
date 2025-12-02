/*    */ package averagingAlgorithms;
/*    */ 
/*    */ public class CriticalChiSquare {
/*    */   private int dof;
/*    */   
/*    */   private double conf;
/*    */   
/*    */   private double value;
/*    */   
/*    */   public CriticalChiSquare(int d, double c) {
/* 25 */     setDOF(d);
/* 26 */     this.conf = c;
/* 27 */     setValue();
/*    */   }
/*    */   
/*    */   public final void setDOF(int d) {
/* 35 */     this.dof = Math.min(d, 340);
/*    */   }
/*    */   
/*    */   public final void setValue() {
/* 47 */     double k = this.dof / 2.0D;
/* 48 */     this.value = 2.0D * 
/* 49 */       MathSpecialFunctions.invLowerIncompleteGamma(
/* 50 */         k, this.conf * MathSpecialFunctions.GammaFunction(k));
/*    */   }
/*    */   
/*    */   public double getValue(boolean reduced) {
/*    */     double result;
/* 62 */     if (reduced) {
/* 63 */       result = this.value / this.dof;
/*    */     } else {
/* 65 */       result = this.value;
/*    */     } 
/* 67 */     return result;
/*    */   }
/*    */   
/*    */   public double getValue() {
/* 74 */     return getValue(false);
/*    */   }
/*    */   
/*    */   public boolean compare(int d, double c) {
/* 86 */     return (this.dof == d && this.conf == c);
/*    */   }
/*    */ }


/* Location:              D:\X\ND\ENSDF\AverageTool_22January2025.jar!\averagingAlgorithms\CriticalChiSquare.class
 * Java compiler version: 8 (52.0)
 * JD-Core Version:       1.1.3
 */