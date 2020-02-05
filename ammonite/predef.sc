// Based on https://gist.github.com/mpilquist/0b1cc1926bddd31c70ad40663acfec8e

// To activate this file make a symlink:
// ln -s ~/.configs/ammonite/predef.sc ~/.ammonite/predef.sc

import $plugin.$ivy.`org.typelevel:::kind-projector:0.11.0`

interp.configureCompiler(_.settings.Ydelambdafy.tryToSetColon(List("inline")))

object importer {

  /**
    * To use fs2 from ammonite repl, type `importer.fs2()` from repl prompt.
    * You'll get all fs2 & cats imports, ContextShift and Timer instances
    * for IO, and a globalBlocker
    */
  def fs2Version(version: String): Unit = {
    repl.load.apply(s"""
      import $$ivy.`co.fs2::fs2-io:$version`, fs2._, fs2.concurrent._, cats._, cats.implicits._, cats.effect._, cats.effect.implicits._, scala.concurrent.duration._

      implicit val ioContextShift: ContextShift[IO] = IO.contextShift(scala.concurrent.ExecutionContext.Implicits.global)
      implicit val ioTimer: Timer[IO] = IO.timer(scala.concurrent.ExecutionContext.Implicits.global)
    """)
    if (!version.startsWith("1")) repl.load.apply("""
      val globalBlocker: Blocker = cats.effect.Blocker.liftExecutionContext(scala.concurrent.ExecutionContext.Implicits.global)
    """)
  }

  def fs2 = fs2Version("2.1.0")

  def circe: Unit = {
    val version ="0.12.3"
    repl.load.apply(s"""
      import $$ivy.`io.circe::circe-core:$version`
      import $$ivy.`io.circe::circe-parser:$version`
      import $$ivy.`io.circe::circe-generic:$version`
      import $$ivy.`io.circe::circe-generic-extras:0.12.2`
      import $$ivy.`io.circe::circe-derivation:0.12.0-M7`
    """)
  }
}
