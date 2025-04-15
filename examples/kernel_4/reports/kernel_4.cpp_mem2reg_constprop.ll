; ModuleID = 'kernel_4.cpp_mem2reg.ll'
source_filename = "src/kernel_4.cpp"
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-unknown-linux-gnu"

; Function Attrs: noinline nounwind uwtable
define i32 @_Z8kernel_4iiii(i32 %a, i32 %b, i32 %c, i32 %n) #0 {
entry:
  br label %for.body

for.body:                                         ; preds = %entry, %for.inc
  %a.addr.03 = phi i32 [ %a, %entry ], [ %rem, %for.inc ]
  %i.02 = phi i32 [ 0, %entry ], [ %inc, %for.inc ]
  %c.addr.01 = phi i32 [ %c, %entry ], [ %add11, %for.inc ]
  %add = add nsw i32 %b, 50
  %add1 = add nsw i32 100, %n
  %mul = mul nsw i32 %add, %add1
  %add2 = add nsw i32 40, %c.addr.01
  %mul3 = mul nsw i32 %mul, %add2
  %add4 = add nsw i32 10, %a.addr.03
  %mul5 = mul nsw i32 %mul3, %add4
  %add6 = add nsw i32 %n, %c.addr.01
  %div = sdiv i32 %mul5, %add6
  %add7 = add nsw i32 %div, %c.addr.01
  %rem = srem i32 %b, %add7
  %mul8 = mul nsw i32 %rem, %n
  %add9 = add nsw i32 %c.addr.01, %b
  %mul10 = mul nsw i32 %add9, %b
  %xor = xor i32 %mul8, %mul10
  %add11 = add nsw i32 %c.addr.01, %xor
  br label %for.inc

for.inc:                                          ; preds = %for.body
  %inc = add nsw i32 %i.02, 1
  %cmp = icmp slt i32 %inc, 100
  br i1 %cmp, label %for.body, label %for.end

for.end:                                          ; preds = %for.inc
  %c.addr.0.lcssa = phi i32 [ %add11, %for.inc ]
  ret i32 %c.addr.0.lcssa
}

; Function Attrs: noinline norecurse nounwind uwtable
define i32 @main() #1 {
entry:
  %call = call i32 @rand() #3
  %rem = srem i32 %call, 10
  %call1 = call i32 @rand() #3
  %rem2 = srem i32 %call1, 10
  %call3 = call i32 @rand() #3
  %rem4 = srem i32 %call3, 10
  %call5 = call i32 @rand() #3
  %rem6 = srem i32 %call5, 10
  %call7 = call i32 @_Z8kernel_4iiii(i32 %rem, i32 %rem2, i32 %rem4, i32 %rem6)
  ret i32 0
}

; Function Attrs: nounwind
declare i32 @rand() #2

attributes #0 = { noinline nounwind uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { noinline norecurse nounwind uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #2 = { nounwind "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #3 = { nounwind }

!llvm.module.flags = !{!0}
!llvm.ident = !{!1}

!0 = !{i32 1, !"wchar_size", i32 4}
!1 = !{!"clang version 6.0.1 (http://github.com/llvm-mirror/clang 2f27999df400d17b33cdd412fdd606a88208dfcc) (http://github.com/llvm-mirror/llvm 5136df4d089a086b70d452160ad5451861269498)"}
